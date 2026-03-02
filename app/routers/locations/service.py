from typing import List, Optional

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.errors import not_found
from app.models.location import Location
from app.routers.locations.schemas import LocationCreate, LocationUpdate


async def create_location(session: AsyncSession, data: LocationCreate) -> Location:
    loc = Location.model_validate(data)
    session.add(loc)
    await session.commit()
    await session.refresh(loc)
    return loc


async def list_locations(session: AsyncSession, city: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Location]:
    stmt = select(Location)
    if city:
        stmt = stmt.where(func.lower(Location.city) == city.lower())
    stmt = stmt.limit(limit).offset(offset)
    res = await session.exec(stmt)
    return list(res.all())


async def get_location(session: AsyncSession, location_id: int) -> Location:
    loc = await session.get(Location, location_id)
    if not loc:
        raise not_found("Location")
    return loc


async def update_location(session: AsyncSession, location_id: int, data: LocationUpdate) -> Location:
    loc = await get_location(session, location_id)
    patch = data.model_dump(exclude_unset=True)
    for k, v in patch.items():
        setattr(loc, k, v)
    session.add(loc)
    await session.commit()
    await session.refresh(loc)
    return loc


async def delete_location(session: AsyncSession, location_id: int) -> None:
    loc = await get_location(session, location_id)
    await session.delete(loc)
    await session.commit()
