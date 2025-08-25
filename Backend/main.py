from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import csv_utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/sites")
async def site():
    return csv_utils.csv_to_json("data/Site Metadata.csv")


@app.get("/water_quality/{site_id}")
async def water_quality(site_id: str):
    site_data = []
    data = csv_utils.csv_to_json("data/water_quality_data.csv")
    for row in data:
        if row["site_id"] == site_id:
            site_data.append(row)
    return site_data

@app.get("/water_quality/{site_id}/date/{date}")
async def water_quality(site_id: str, date: str):
    site_data = []
    data = csv_utils.csv_to_json("data/water_quality_data.csv")
    for row in data:
        if row["site_id"] == site_id and row["date"] == date:
            site_data.append(row)
    return site_data

