from pydantic import BaseModel, Field, ConfigDict
from datetime import date

from typing import List

class StaffBase(BaseModel):
    name: str = Field(..., max_length=30)
    surname: str = Field(..., max_length=30)
    start_work: date = Field(...)
    job_title: str = Field(..., max_length=40)

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    name: str | None= Field(..., max_length=30)
    surname: str | None= Field(..., max_length=30)
    start_work: date | None= Field(...)
    job_title: str | None= Field(..., max_length=40)

class StaffResponse(StaffBase):
    id: int
    station_id: int

    model_config = ConfigDict(from_attributes=True)