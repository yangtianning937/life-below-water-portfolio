from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, field_validator, BaseModel


class Activity(BaseModel):
    name: str
    description: str
    location: str
    date: datetime
    start: datetime
    end: datetime
    tags: list[str]
    image: str
    model_config = ConfigDict(extra="ignore")

    @field_validator("date", "start", "end", mode="before")
    @classmethod
    def parse_zulu(cls, v):
        if isinstance(v, str) and v.endswith("Z"):
            v = v.replace("Z", "+00:00")
        return v


class Form(BaseModel):
    name: str
    activity_id: str
    email: str
    requirements: Optional[str] = None
    parents: list[str]