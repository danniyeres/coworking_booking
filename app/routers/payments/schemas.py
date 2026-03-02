from typing import Optional
from decimal import Decimal

from sqlmodel import Field, SQLModel


class PaymentCreate(SQLModel):
    booking_id: int
    amount: Decimal


class PaymentUpdate(SQLModel):
    amount: Optional[Decimal] = None
    status: Optional[str] = Field(default=None, max_length=50)


class PaymentRead(SQLModel):
    id: int
    booking_id: int
    amount: Decimal
    status: str
