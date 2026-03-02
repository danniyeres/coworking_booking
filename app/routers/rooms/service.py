from typing import List, Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.errors import not_found
from app.models.location import Location
from app.models.room import Room
from app.routers.rooms.schemas import RoomCreate, RoomUpdate


async def create_room(session: AsyncSession, data: RoomCreate) -> Room:
    if not await session.get(Location, data.location_id):
        raise not_found("Location")
    room = Room.model_validate(data)
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


async def list_rooms(session: AsyncSession, location_id: Optional[int] = None, limit: int = 50, offset: int = 0) -> List[Room]:
    stmt = select(Room)
    if location_id:
        stmt = stmt.where(Room.location_id == location_id)
    stmt = stmt.limit(limit).offset(offset)
    res = await session.exec(stmt)
    return list(res.all())


async def get_room(session: AsyncSession, room_id: int) -> Room:
    room = await session.get(Room, room_id)
    if not room:
        raise not_found("Room")
    return room


async def update_room(session: AsyncSession, room_id: int, data: RoomUpdate) -> Room:
    room = await get_room(session, room_id)
    patch = data.model_dump(exclude_unset=True)
    if "location_id" in patch and not await session.get(Location, patch["location_id"]):
        raise not_found("Location")
    for k, v in patch.items():
        setattr(room, k, v)
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room


async def delete_room(session: AsyncSession, room_id: int) -> None:
    room = await get_room(session, room_id)
    await session.delete(room)
    await session.commit()
