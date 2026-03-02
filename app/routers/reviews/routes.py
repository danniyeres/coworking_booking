from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.routers.reviews import service
from app.routers.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter()


@router.post("", response_model=ReviewRead, status_code=201)
async def create_review(payload: ReviewCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_review(session, payload)


@router.get("", response_model=List[ReviewRead])
async def list_reviews(
    location_id: Optional[int] = None,
    user_id: Optional[int] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_reviews(session, location_id=location_id, user_id=user_id, limit=limit, offset=offset)


@router.get("/{review_id}", response_model=ReviewRead)
async def get_review(review_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_review(session, review_id)


@router.put("/{review_id}", response_model=ReviewRead)
async def update_review(review_id: int, payload: ReviewUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_review(session, review_id, payload)


@router.delete("/{review_id}", status_code=204)
async def delete_review(review_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_review(session, review_id)
    return None
