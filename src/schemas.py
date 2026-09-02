from pydantic import BaseModel, Field, ConfigDict 
from typing import List

class ScooterBase(BaseModel):
    model: str = Field(..., max_length=100)
    battery_level: float = Field(..., ge=0, le=100)
    is_available: bool = True
    location: Optional[str] = Field(..., max_length=200)

class ScooterCreate(ScooterBase):
    pass

class ScooterUpdate(BaseModel):
    model: str | None = Field(None, max_length=100)
    battery_level: float | None = Field(None, ge=0, le=100)
    is_available: bool | None = None
    location: str | None = Field(None, max_length=200)
    station_id: int | None = None

class ScooterReturn(BaseModel):
    location: str = Field(..., max_length=200)
    battery_level: float | None = Field(None, ge=0, le=100)


class ScooterResponse(ScooterBase):
    station_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)

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

    model_config = ConfigDict(from_attributes=True)