from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.routers.rooms import service
from app.routers.rooms.schemas import RoomCreate, RoomRead, RoomUpdate

router = APIRouter()


@router.post("", response_model=RoomRead, status_code=201)
async def create_room(payload: RoomCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_room(session, payload)


@router.get("", response_model=List[RoomRead])
async def list_rooms(
    location_id: Optional[int] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_rooms(session, location_id=location_id, limit=limit, offset=offset)


@router.get("/{room_id}", response_model=RoomRead)
async def get_room(room_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_room(session, room_id)


@router.put("/{room_id}", response_model=RoomRead)
async def update_room(room_id: int, payload: RoomUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_room(session, room_id, payload)


@router.delete("/{room_id}", status_code=204)
async def delete_room(room_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_room(session, room_id)
    return None
