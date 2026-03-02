from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.routers.locations import service
from app.routers.locations.schemas import LocationCreate, LocationRead, LocationUpdate

router = APIRouter()


@router.post("", response_model=LocationRead, status_code=201)
async def create_location(payload: LocationCreate, session: AsyncSession = Depends(get_session)):
    return await service.create_location(session, payload)


@router.get("", response_model=List[LocationRead])
async def list_locations(
    city: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_locations(session, city=city, limit=limit, offset=offset)


@router.get("/{location_id}", response_model=LocationRead)
async def get_location(location_id: int, session: AsyncSession = Depends(get_session)):
    return await service.get_location(session, location_id)


@router.put("/{location_id}", response_model=LocationRead)
async def update_location(location_id: int, payload: LocationUpdate, session: AsyncSession = Depends(get_session)):
    return await service.update_location(session, location_id, payload)


@router.delete("/{location_id}", status_code=204)
async def delete_location(location_id: int, session: AsyncSession = Depends(get_session)):
    await service.delete_location(session, location_id)
    return None
