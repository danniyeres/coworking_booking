from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.routers.bookings import service
from app.routers.bookings.schemas import BookingCreate, BookingRead, BookingUpdate

router = APIRouter()


@router.post("", response_model=BookingRead, status_code=201)
async def create_booking(payload: BookingCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_booking(session, payload)


@router.get("", response_model=List[BookingRead])
async def list_bookings(
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
    date_from: Optional[datetime] = Query(default=None, description="ISO datetime: start_time >= date_from"),
    date_to: Optional[datetime] = Query(default=None, description="ISO datetime: end_time <= date_to"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_bookings(
        session,
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )


@router.get("/{booking_id}", response_model=BookingRead)
async def get_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_booking(session, booking_id)


@router.put("/{booking_id}", response_model=BookingRead)
async def update_booking(booking_id: int, payload: BookingUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_booking(session, booking_id, payload)


@router.delete("/{booking_id}", status_code=204)
async def delete_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_booking(session, booking_id)
    return None
