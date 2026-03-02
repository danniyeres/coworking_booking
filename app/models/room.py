
from sqlmodel import Field, Relationship, SQLModel

class Room(SQLModel, table=True):
    __tablename__ = "rooms"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    capacity: int = Field(nullable=False)
    price_per_hour: float = Field(nullable=False)

    location_id: int = Field(foreign_key="locations.id", nullable=False, index=True)

    location: "Location" = Relationship(
        back_populates="rooms",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    bookings: list["Booking"] = Relationship(
        back_populates="room",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
