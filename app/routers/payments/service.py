from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.errors import conflict, not_found
from app.models.booking import Booking
from app.models.payment import Payment
from app.routers.payments.schemas import PaymentCreate, PaymentUpdate


async def create_payment(session: AsyncSession, data: PaymentCreate) -> Payment:
    if not await session.get(Booking, data.booking_id):
        raise not_found("Booking")

    payment = Payment(
        booking_id=data.booking_id,
        amount=data.amount,
        status="PENDING",
    )

    session.add(payment)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise conflict("Payment for this booking already exists")
    await session.refresh(payment)
    return payment


async def list_payments(session: AsyncSession, booking_id: Optional[int] = None, limit: int = 50, offset: int = 0) -> List[Payment]:
    stmt = select(Payment)
    if booking_id:
        stmt = stmt.where(Payment.booking_id == booking_id)
    stmt = stmt.limit(limit).offset(offset)
    res = await session.exec(stmt)
    return list(res.all())


async def get_payment(session: AsyncSession, payment_id: int) -> Payment:
    payment = await session.get(Payment, payment_id)
    if not payment:
        raise not_found("Payment")
    return payment


async def update_payment(session: AsyncSession, payment_id: int, data: PaymentUpdate) -> Payment:
    payment = await get_payment(session, payment_id)
    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(payment, k, v)
    session.add(payment)
    await session.commit()
    await session.refresh(payment)
    return payment


async def delete_payment(session: AsyncSession, payment_id: int) -> None:
    payment = await get_payment(session, payment_id)
    await session.delete(payment)
    await session.commit()
