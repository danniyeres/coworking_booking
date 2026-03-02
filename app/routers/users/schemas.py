from typing import Optional
from sqlmodel import Field, SQLModel


class UserCreate(SQLModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=5, max_length=255)


class UserUpdate(SQLModel):
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    email: Optional[str] = Field(default=None, min_length=5, max_length=255)


class UserRead(SQLModel):
    id: int
    full_name: str
    email: str
