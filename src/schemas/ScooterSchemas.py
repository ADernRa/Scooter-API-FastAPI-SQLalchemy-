from pydantic import BaseModel, Field, ConfigDict 
from typing import List
from src.schemas.RideSchemas import RideResponde

class ScooterBase(BaseModel):
    model: str = Field(..., max_length=100)
    battery_level: float = Field(..., ge=0, le=100)
    is_available: bool = True
    location: str = Field(..., max_length=200)
    price: float = Field(...)
    
class ScooterCreate(ScooterBase):
    pass

class ScooterUpdate(BaseModel):
    model: str | None = Field(None, max_length=100)
    battery_level: float | None = Field(None, ge=0, le=100)
    is_available: bool | None = None
    location: str | None = Field(None, max_length=200)
    price: float | None = Field(..., ge=0.0)
    station_id: int | None = None

class ScooterReturn(BaseModel):
    location: str = Field(..., max_length=200)
    battery_level: float | None = Field(None, ge=0, le=100)


class ScooterResponse(ScooterBase):
    station_id: int
    id: int

    rides: List[RideResponde] = []

    model_config = ConfigDict(from_attributes=True)