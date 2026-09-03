from src.dependencies import verify_admin
from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from typing import List
from sqlalchemy.orm import selectinload

from src.database import get_db
from src.models import Station, Scooter
from src.schemas.ScooterSchemas import (
    ScooterCreate, ScooterResponse, ScooterUpdate
)
from src.schemas.SationSchemas import (
    StationCreate, StationResponse, StationUpdate
)

admin_router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admins"],
    dependencies=[Depends(verify_admin)]  
)

# Список станцій
@admin_router.get("stations", response_model=List[StationResponse])
async def get_stations(db: AsyncSession = Depends(get_db)):
    query = select(Station).options(
        selectinload(Station.scooters),
        selectinload(Station.staff)
        )
    result = await db.execute(query)
    stations = result.scalars().all()
    print(stations)
    return stations

# Створити станцію
@admin_router.post("/stations", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
async def create_station(station: StationCreate, db: AsyncSession = Depends(get_db)):
    new_station = Station(**station.model_dump())
    db.add(new_station)
    await db.commit()
    await db.refresh(new_station, attribute_names=["scooters", "staff"])
    print(new_station)
    return new_station

# Створити самокат
@admin_router.post("/stations/{station_id}/scooters", response_model=ScooterResponse, status_code=status.HTTP_201_CREATED)
async def create_scooter(station_id: int, scooter: ScooterCreate, db: AsyncSession = Depends(get_db)):
    query = select(Station).where(Station.id == station_id)
    result = await db.execute(query)
    station = result.scalar_one_or_none()
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    new_scooter = Scooter(**scooter.model_dump(), station_id=station_id)
    db.add(new_scooter)
    await db.commit()
    await db.refresh(new_scooter)
    print(new_scooter)
    return new_scooter

# Видалити станцію
@admin_router.delete("/stations/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stations(station_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Station).where(Station.id == station_id)
    result = await db.execute(query)
    station = result.scalar_one_or_none()

    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    # Якщо хочаб один самокат належить станції, то видалити неможливо
    query = select(func.count(Scooter.id)).where(Scooter.station_id == station_id)
    result = await db.execute(query)
    scooters_count = result.scalar() or 0

    if scooters_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN , 
            detail=f"There are still scooters at the station {scooters_count}."
        )
    
    delete_query = delete(Station).where(Station.id == station_id)
    await db.execute(delete_query)
    await db.commit()
    return None

# Видалити самокат
@admin_router.delete("/scooters/{scooter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scooter(scooter_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Scooter).where(Scooter.id == scooter_id)
    result = await db.execute(query)
    scooter = result.scalar_one_or_none()
    
    if not scooter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scooter not found")
    
    delete_query = delete(Scooter).where(Scooter.id == scooter_id)
    await db.execute(delete_query)
    await db.commit()
    return None

# Оновлення інформації про станцію
@admin_router.patch("/stations/{station_id}", response_model=StationResponse)
async def update_station(
    station_id: int,
    station_data: StationUpdate,
    db: AsyncSession = Depends(get_db)
    ):

    query = select(Station).where(Station.id == station_id)
    result = await db.execute(query)
    station = result.scalar_one_or_none()
    
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
    
    update_dict = station_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(station, key, value)

    await db.commit()
    await db.refresh(station, attribute_names=["scooters", "staff"])
    return station

# Оновлення інформації про самокат
@admin_router.patch("/scooters/{scooter_id}", response_model=ScooterResponse)
async def update_scooter(
    scooter_id: int,
    scooter_data: ScooterUpdate,
    db: AsyncSession = Depends(get_db)
    ):

    query = select(Scooter).where(Scooter.id == scooter_id)
    result = await db.execute(query)
    scooter = result.scalar_one_or_none()
    
    if not scooter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scooter not found")

    if scooter_data.station_id is not None:
        station = await db.execute(select(Station).where(Station.id == scooter_data.station_id))
        if not station.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"It is not possible to lock the scooter. Stations with ID {scooter_data.station_id} does not exist"
            )

    update_dict = scooter_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(scooter, key, value)

    await db.commit()
    await db.refresh(scooter)
    return scooter