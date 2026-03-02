
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class Location(SQLModel, table=True):
    __tablename__ = "locations"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    address: str = Field(nullable=False, max_length=255)
    city: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    rooms: list["Room"] = Relationship(
        back_populates="location",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    reviews: list["Review"] = Relationship(
        back_populates="location",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
