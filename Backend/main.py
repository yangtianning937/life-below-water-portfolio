import uuid
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import JSONResponse

import csv_utils

# python -m uvicorn Backend.main:app --reload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


site_metadata = csv_utils.csv_to_json("data/Site Metadata.csv")
water_quality = csv_utils.csv_to_json("data/water_quality_data.csv")


class PostActivity(BaseModel):
    name: str
    description: str
    location: str
    date: datetime
    start: datetime
    end: datetime
    tags: list[str]


##################
# APIs for Epic 1
##################
@app.get("/sites")
async def site():
    return site_metadata


@app.get("/water_quality/{site_id}")
async def water_quality(site_id: str):
    site_data = []
    for row in water_quality:
        if row["site_id"] == site_id:
            site_data.append(row)
    return site_data

@app.get("/water_quality/{site_id}/date/{date}")
async def water_quality(site_id: str, date: str):
    site_data = []
    for row in water_quality:
        if row["site_id"] == site_id and row["date"] == date:
            site_data.append(row)
    return site_data


##################
# APIs for Epic 2
##################
@app.post("/activity")
async def post_activity(activity: PostActivity):
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

        csv_utils.json_to_csv("data/activity_data.csv", activity_data)

        return JSONResponse(content={"msg": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=500)

