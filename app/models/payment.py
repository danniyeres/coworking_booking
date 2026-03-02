
from sqlmodel import Field, Relationship, SQLModel

class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: int | None = Field(default=None, primary_key=True)
    amount: float = Field(nullable=False)
    status: str = Field(default="PENDING", max_length=50)

    booking_id: int = Field(foreign_key="bookings.id", nullable=False, index=True)

    booking: "Booking" = Relationship(
        back_populates="payment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
