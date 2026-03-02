from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.routers.users import service
from app.routers.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("", response_model=UserRead, status_code=201)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_user(session, payload)


@router.get("", response_model=List[UserRead])
async def list_users(
    email: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_users(session, email=email, limit=limit, offset=offset)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_user(session, user_id)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, payload: UserUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_user(session, user_id, payload)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_user(session, user_id)
    return None
