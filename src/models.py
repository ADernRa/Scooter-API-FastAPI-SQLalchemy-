from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, Float, Integer
from typing import List

class Base(DeclarativeBase):
    pass

class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    adress: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    scooters: Mapped[List["Scooter"]] = relationship("Scooter", back_populates="station")

class Scooter(Base):
    __tablename__ = "scooters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    battery_level: Mapped[float] = mapped_column(Float, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    station_id: Mapped[int] = mapped_column(ForeignKey("stations.id"), nullable=False)

    station: Mapped["Station"] = relationship("Station", back_populates="scooters")