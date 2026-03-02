from typing import List, Optional
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.errors import bad_request, not_found
from app.models.booking import Booking
from app.models.room import Room
from app.models.user import User
from app.routers.bookings.schemas import BookingCreate, BookingUpdate


def _validate_time_range(start: datetime, end: datetime) -> None:
    if end <= start:
        raise bad_request("end_time must be greater than start_time")


async def create_booking(session: AsyncSession, data: BookingCreate) -> Booking:
    _validate_time_range(data.start_time, data.end_time)

    if not await session.get(User, data.user_id):
        raise not_found("User")
    if not await session.get(Room, data.room_id):
        raise not_found("Room")

    booking = Booking.model_validate(data)
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking


async def list_bookings(
    session: AsyncSession,
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Booking]:
    stmt = select(Booking)
    if user_id:
        stmt = stmt.where(Booking.user_id == user_id)
    if room_id:
        stmt = stmt.where(Booking.room_id == room_id)
    if date_from:
        stmt = stmt.where(Booking.start_time >= date_from)
    if date_to:
        stmt = stmt.where(Booking.end_time <= date_to)

    stmt = stmt.order_by(Booking.start_time.desc()).limit(limit).offset(offset)
    res = await session.exec(stmt)
    return list(res.all())


async def get_booking(session: AsyncSession, booking_id: int) -> Booking:
    booking = await session.get(Booking, booking_id)
    if not booking:
        raise not_found("Booking")
    return booking


async def update_booking(session: AsyncSession, booking_id: int, data: BookingUpdate) -> Booking:
    booking = await get_booking(session, booking_id)
    patch = data.model_dump(exclude_unset=True)

    if "user_id" in patch and not await session.get(User, patch["user_id"]):
        raise not_found("User")
    if "room_id" in patch and not await session.get(Room, patch["room_id"]):
        raise not_found("Room")

    new_start = patch.get("start_time", booking.start_time)
    new_end = patch.get("end_time", booking.end_time)
    _validate_time_range(new_start, new_end)

    for k, v in patch.items():
        setattr(booking, k, v)

    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking


async def delete_booking(session: AsyncSession, booking_id: int) -> None:
    booking = await get_booking(session, booking_id)
    await session.delete(booking)
    await session.commit()
