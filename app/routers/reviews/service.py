from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.errors import not_found
from app.models.location import Location
from app.models.review import Review
from app.models.user import User
from app.routers.reviews.schemas import ReviewCreate, ReviewUpdate


async def create_review(session: AsyncSession, data: ReviewCreate) -> Review:
    if not await session.get(User, data.user_id):
        raise not_found("User")
    if not await session.get(Location, data.location_id):
        raise not_found("Location")

    review = Review.model_validate(data)
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def list_reviews(
    session: AsyncSession,
    location_id: Optional[int] = None,
    user_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Review]:
    stmt = select(Review)
    if location_id:
        stmt = stmt.where(Review.location_id == location_id)
    if user_id:
        stmt = stmt.where(Review.user_id == user_id)
    stmt = stmt.order_by(Review.id.desc()).limit(limit).offset(offset)
    res = await session.exec(stmt)
    return list(res.all())


async def get_review(session: AsyncSession, review_id: int) -> Review:
    review = await session.get(Review, review_id)
    if not review:
        raise not_found("Review")
    return review


async def update_review(session: AsyncSession, review_id: int, data: ReviewUpdate) -> Review:
    review = await get_review(session, review_id)
    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(review, k, v)
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def delete_review(session: AsyncSession, review_id: int) -> None:
    review = await get_review(session, review_id)
    await session.delete(review)
    await session.commit()
