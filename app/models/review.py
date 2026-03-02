
from sqlmodel import Field, Relationship, SQLModel

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: int | None = Field(default=None, primary_key=True)
    rating: int = Field(nullable=False)
    comment: str | None = Field(default=None)

    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    location_id: int = Field(foreign_key="locations.id", nullable=False, index=True)

    user: "User" = Relationship(
        back_populates="reviews",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    location: "Location" = Relationship(
        back_populates="reviews",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
