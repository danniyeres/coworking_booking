from typing import Optional
from sqlmodel import Field, SQLModel


class LocationCreate(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    city: str = Field(min_length=1, max_length=100)


class LocationUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    address: Optional[str] = Field(default=None, min_length=1, max_length=255)
    city: Optional[str] = Field(default=None, min_length=1, max_length=100)


class LocationRead(SQLModel):
    id: int
    name: str
    address: str
    city: str
