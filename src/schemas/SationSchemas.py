from pydantic import BaseModel, Field, ConfigDict 
from typing import List

from src.schemas.ScooterSchemas import ScooterResponse
from src.schemas.SatffSchemas import StaffResponse

class StationBase(BaseModel):
    name: str = Field(..., max_length=100)
    address: str = Field(..., max_length=200)
    is_active: bool = True

class StationCreate(StationBase):
    pass

class StationUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    address: str | None = Field(None, max_length=200)
    is_active: bool | None = None

class StationResponse(StationBase):
    id: int

    scooters: List[ScooterResponse] = []
    staff: List[StaffResponse] = []


    model_config = ConfigDict(from_attributes=True)