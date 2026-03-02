from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class BookingCreate(SQLModel):
    user_id: int
    room_id: int
    start_time: datetime
    end_time: datetime


class BookingUpdate(SQLModel):
    user_id: Optional[int] = None
    room_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = Field(default=None, max_length=50)


class BookingRead(SQLModel):
    id: int
    user_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    status: str
