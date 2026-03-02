from typing import Optional

from sqlmodel import Field, SQLModel


class ReviewCreate(SQLModel):
    user_id: int
    location_id: int
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1, max_length=1000)


class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = Field(default=None, min_length=1, max_length=1000)


class ReviewRead(SQLModel):
    id: int
    user_id: int
    location_id: int
    rating: int
    comment: str
