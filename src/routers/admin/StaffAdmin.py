from src.dependencies import verify_admin
from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from typing import List
from sqlalchemy.orm import selectinload

from src.database import get_db
from src.models import Station, Staff

from src.schemas.StaffSchemas import (
    StaffCreate, StaffUpdate, StaffResponse
)

admin_router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admins"],
    dependencies=[Depends(verify_admin)]  
)

@admin_router.post("station/{station_id}/staff", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(station_id: int, staff: StaffCreate, db: AsyncSession = Depends(get_db)):
    query = select(Station).where(Station.id == station_id)
    result = await db.execute(query)
    station = result.scalar_one_or_none()
    if not station:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    new_staff = Staff(**staff.model_dump(), station_id=station_id)
    db.add(new_staff)
    await db.commit()
    await db.refresh(new_staff)
    return new_staff

@admin_router.get("station/{station_id}/staff", response_model=List[StaffResponse], status_code=status.HTTP_201_CREATED)
async def get_staff(station_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Staff).where(Staff.station_id == station_id)
    result = await db.execute(query)
    staff = result.scalars().all()
    return staff