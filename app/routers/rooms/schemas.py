from typing import Optional
from decimal import Decimal

from sqlmodel import Field, SQLModel


class RoomCreate(SQLModel):
    location_id: int
    name: str = Field(min_length=1, max_length=255)
    capacity: int = Field(ge=1)
    price_per_hour: Decimal


class RoomUpdate(SQLModel):
    location_id: Optional[int] = None
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    capacity: Optional[int] = Field(default=None, ge=1)
    price_per_hour: Optional[Decimal] = None


class RoomRead(SQLModel):
    id: int
    location_id: int
    name: str
    capacity: int
    price_per_hour: Decimal
