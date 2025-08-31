import uuid
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import JSONResponse, FileResponse

import csv_utils
from Backend.dynamic_CORS_middleware import DynamicCORSMiddleware
from Backend.request_model import Activity, Form

# python -m uvicorn Backend.main:app --reload

app = FastAPI()
app.add_middleware(DynamicCORSMiddleware)

site_metadata = csv_utils.csv_to_json("data/Site Metadata.csv")
water_quality = csv_utils.csv_to_json("data/water_quality_data.csv")


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(status_code=422, content={"detail": exc.errors()})


##################
# APIs for Epic 1
##################
@app.get("/sites")
async def get_sites():
    return site_metadata


@app.get("/water_quality/{site_id}")
async def get_water_quality(site_id: str):
    site_data = []
    for row in water_quality:
        if row["site_id"] == site_id:
            site_data.append(row)
    return site_data


@app.get("/water_quality/{site_id}/date/{date}")
async def get_water_quality(site_id: str, date: str):
    site_data = []
    for row in water_quality:
        if row["site_id"] == site_id and row["date"] == date:
            site_data.append(row)
    return site_data


##################
# APIs for Epic 2
##################
@app.post("/activity")
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


@app.get("/activity")
async def get_activity():
    return csv_utils.csv_to_json("data/activity_data.csv")


@app.get("/activity/{activity_id}")
async def get_activity(activity_id: str):
    activity_data = []
    activity = csv_utils.csv_to_json("data/activity_data.csv")
    for row in activity:
        if row["id"] == activity_id:
            activity_data.append(row)

    return activity_data


@app.post("/activity/form")
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
# Other APIs
##################
@app.get("/image/{name}")
async def get_image(name: str):
    image_path = Path(f"img/{name}")
    if not image_path.is_file():
        return JSONResponse(content={"msg": "not found"}, status_code=404)
    else:
        return FileResponse(image_path)
