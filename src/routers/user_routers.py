from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from src.database import get_db
from src.models import Station, Scooter

from src.schemas.ScooterSchemas import (
    ScooterCreate, ScooterResponse, ScooterUpdate, ScooterReturn
)
from src.schemas.SationSchemas import (
    StationCreate, StationResponse, StationUpdate
)

router = APIRouter(
    prefix="/api/v1/user", 
    tags=["users"]
    )

# Отримати інформацію про незайняті самокати
@router.get("/{station_id}/scooters/available", response_model=List[ScooterResponse])
async def get_avaible_scooter(station_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Scooter).where(Scooter.station_id == station_id, Scooter.is_available == True)
    result = await db.execute(query)
    scooters = result.scalars().all()
    print(scooters)
    return scooters

# Арендувати самокат
@router.patch("/{station_id}/scooters/{scooter_id}/rent", response_model=ScooterResponse)
async def rent_scooter(station_id: int, scooter_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Scooter).where(Scooter.id == scooter_id, Scooter.station_id == station_id) 
    result = await db.execute(query)
    scooter = result.scalar_one_or_none()

    if not scooter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scooter not found")

    if not scooter.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Scooter is not available")

    scooter.is_available = False
    await db.commit()
    await db.refresh(scooter)
    return scooter

# Припинити аренду самокату
@router.patch("/{station_id}/scooters/{scooter_id}/return", response_model=ScooterResponse)
async def return_scooter(station_id: int, scooter_id: int, return_data: ScooterReturn, db: AsyncSession = Depends(get_db)):

    query = select(Scooter).where(Scooter.id == scooter_id, Scooter.station_id == station_id) 
    result = await db.execute(query)
    scooter = result.scalar_one_or_none()

    if not scooter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scooter not found")

    if scooter.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Scooter is already at a station and is not rented")

    scooter.is_available = True
    scooter.location = return_data.location

    if return_data.battery_level is not None:
        scooter.battery_level = return_data.battery_level

    await db.commit()
    await db.refresh(scooter)
    return scooter
