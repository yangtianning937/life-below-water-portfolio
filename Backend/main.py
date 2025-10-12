import uuid
from datetime import datetime
from pathlib import Path

import requests
from fastapi import FastAPI, Depends, APIRouter, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from utils import csv_utils
from geocode.geocode import reverse_geocode_service, places_autocomplete_service, place_details_service, \
    places_find_service
from db.db import get_db
from db.models import SiteMetadata, WaterQualityData
from dynamic_cors_middleware import DynamicCORSMiddleware
from recommend.process import analyze_nearby_beaches
from request_model import Activity, Form

# python -m uvicorn Backend.main:app --reload
# ssh -i path/to/Group26.pem -N -L 6543:waterqdb.cpmwumooifyh.ap-southeast-2.rds.amazonaws.com:5432 ubuntu@<PUBLIC_IP>

app = FastAPI()
app.add_middleware(DynamicCORSMiddleware)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

api = APIRouter(prefix="/api", tags=["api"])

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(status_code=422, content={"detail": exc.errors()})

##################
# APIs for Epic 1
##################
@api.get("/sites")
async def get_sites(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(SiteMetadata).order_by(SiteMetadata.site_id))
    return res.scalars().all()


@api.get("/water_quality/{site_id}")
async def get_water_quality(site_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(WaterQualityData).where(WaterQualityData.site_id == site_id)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return rows


@api.get("/water_quality/{site_id}/date/{date}")
async def get_water_quality(site_id: str, date: str, db: AsyncSession = Depends(get_db)):
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Invalid date format, must be YYYY-MM-DD"}

    stmt = select(WaterQualityData).where(
        WaterQualityData.site_id == site_id,
        WaterQualityData.date == parsed_date
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return rows


##################
# APIs for Epic 2
##################
@api.post("/activity")
async def post_activity(activity: Activity):
    try:
        activity_data = [
            {
                "id": uuid.uuid4().hex,
                "name": activity.name,
                "description": activity.description,
                "location": activity.location,
                "date": activity.date,
                "start": activity.start,
                "end": activity.end,
                "tags": activity.tags,
            }
        ]

        is_exists = False

        exists_activity = csv_utils.csv_to_json("data/activity_data.csv")
        for row in exists_activity:
            if row.get("name") == activity.name \
                    and row.get("description") == activity.description \
                    and row.get("location") == activity.location \
                    and row.get("date") == str(activity.date) \
                    and row.get("start") == str(activity.start) \
                    and row.get("end") == str(activity.end) \
                    and row.get("tags") == str(activity.tags):
                is_exists = True
                break
        if not is_exists:
            csv_utils.json_to_csv("data/activity_data.csv", activity_data)

            return JSONResponse(content={"msg": "success"}, status_code=200)
        else:
            return JSONResponse(content={"msg": "already exists"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)


@api.get("/activity")
async def get_activity():
    return csv_utils.csv_to_json("data/activity_data.csv")


@api.get("/activity/{activity_id}")
async def get_activity(activity_id: str):
    activity_data = []
    activity = csv_utils.csv_to_json("data/activity_data.csv")
    for row in activity:
        if row["id"] == activity_id:
            activity_data.append(row)

    return activity_data


@api.post("/activity/form")
async def post_activity_form(form: Form):
    try:
        form_data = [{
            "id": uuid.uuid4().hex,
            "activity_id": form.activity_id,
            "full_name": form.full_name,
            "parents": form.parents,
            "email": form.email,
            "requirements": form.requirements,
        }]

        is_exists = False

        exists_form = csv_utils.csv_to_json("data/form_data.csv")
        for row in exists_form:
            if row["activity_id"] == form.activity_id \
                    and row["full_name"] == form.full_name \
                    and row["parents"] == str(form.parents) \
                    and row["email"] == form.email:
                is_exists = True
                break

        if not is_exists:
            csv_utils.json_to_csv("data/form_data.csv", form_data)

            return JSONResponse(content={"msg": "success"}, status_code=200)
        else:
            return JSONResponse(content={"msg": "already exists"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)


##################
# APIs for Epic 3
##################
@api.get("/nearby/{latitude}/{longitude}")
async def get_nearby_beach(latitude: str | float, longitude: str | float):
    try:
        latitude = float(latitude)
        longitude = float(longitude)

        try:
            res = analyze_nearby_beaches(latitude, longitude)
            return res[0]
        except requests.exceptions.HTTPError as e:
            print(f"API request failed: {e}")
            print("Please check if your GOOGLE_API_KEY is correct, or if API quota is exhausted.")
        except Exception as e:
            print(f"An error occurred: {e}")
    except ValueError:
        return JSONResponse(content={"msg": "Invalid latitude or longitude"}, status_code=400)

@api.get("/reverse_geocode/{latitude}/{longitude}")
async def reverse_geocode(latitude: str | float, longitude: str | float):
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        return await reverse_geocode_service(latitude, longitude)
    except ValueError:
        return JSONResponse(content={"msg": "Invalid latitude or longitude"}, status_code=400)

@api.get("/places/autocomplete")
async def places_autocomplete(
    q: str = Query(..., min_length=2),
    country: str = Query("AU"),
    limit: int = Query(8, ge=1, le=10),
    language: str = Query("en")
):
    return JSONResponse(await places_autocomplete_service(q, country, limit, language))

@api.get("/places/details")
async def place_details(
    place_id: str = Query(...),
    language: str = Query("en")
):
    return JSONResponse(await place_details_service(place_id, language))

@api.get("/places/find")
async def places_find(
    q: str = Query(..., min_length=2),
    country: str = Query("AU"),
    language: str = Query("en")
):
    return JSONResponse(await places_find_service(q, country, language))

##################
# Other APIs
##################
@api.get("/image/{name}")
async def get_image(name: str):
    image_path = Path(f"img/{name}")
    if not image_path.is_file():
        return JSONResponse(content={"msg": "not found"}, status_code=404)
    else:
        return FileResponse(image_path)

app.include_router(api)

app.mount("/", StaticFiles(directory="dist", html=True), name="static")