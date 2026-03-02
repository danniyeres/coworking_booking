from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.routers.payments import service
from app.routers.payments.schemas import PaymentCreate, PaymentRead, PaymentUpdate

router = APIRouter()


@router.post("", response_model=PaymentRead, status_code=201)
async def create_payment(payload: PaymentCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_payment(session, payload)


@router.get("", response_model=List[PaymentRead])
async def list_payments(
    booking_id: Optional[int] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_payments(session, booking_id=booking_id, limit=limit, offset=offset)


@router.get("/{payment_id}", response_model=PaymentRead)
async def get_payment(payment_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_payment(session, payment_id)


@router.put("/{payment_id}", response_model=PaymentRead)
async def update_payment(payment_id: int, payload: PaymentUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_payment(session, payment_id, payload)


@router.delete("/{payment_id}", status_code=204)
async def delete_payment(payment_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_payment(session, payment_id)
    return None
