from sqlalchemy import String, Boolean, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from src.models.BaseModel import Base

class Scooter(Base):
    __tablename__ = "scooters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    battery_level: Mapped[float] = mapped_column(Float, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    station_id: Mapped[int] = mapped_column(ForeignKey("stations.id"), nullable=False)

    station: Mapped["Station"] = relationship("Station", back_populates="scooters")
    rides: Mapped[List["Ride"]] = relationship("Ride", back_populates="scooter", lazy="selectin")