from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.errors import conflict, not_found
from app.models.user import User
from app.routers.users.schemas import UserCreate, UserUpdate


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User.model_validate(data)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise conflict("Email already exists")
    await session.refresh(user)
    return user


async def list_users(session: AsyncSession, email: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[User]:
    stmt = select(User)
    if email:
        stmt = stmt.where(User.email == email)
    stmt = stmt.limit(limit).offset(offset)
    res = await session.exec(stmt)
    return list(res.all())


async def get_user(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise not_found("User")
    return user


async def update_user(session: AsyncSession, user_id: int, data: UserUpdate) -> User:
    user = await get_user(session, user_id)
    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(user, k, v)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise conflict("Email already exists")
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await get_user(session, user_id)
    await session.delete(user)
    await session.commit()
