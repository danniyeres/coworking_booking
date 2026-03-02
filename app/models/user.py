
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, unique=True, index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    bookings: list["Booking"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    reviews: list["Review"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
