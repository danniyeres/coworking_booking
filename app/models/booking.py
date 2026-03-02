from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlmodel import Field, Relationship, SQLModel


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    room_id: int = Field(foreign_key="rooms.id", nullable=False, index=True)

    start_time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )
    end_time: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False)
    )

    status: str = Field(default="CREATED", nullable=False, max_length=50)

    user: "User" = Relationship(
        back_populates="bookings",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    room: "Room" = Relationship(
        back_populates="bookings",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    payment: Optional["Payment"] = Relationship(
        back_populates="booking",
        sa_relationship_kwargs={"lazy": "selectin"},
    )