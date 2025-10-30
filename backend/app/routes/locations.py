from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ..database import get_db
from ..models.location import Location
from ..schemas.location import LocationResponse

router = APIRouter(prefix="", tags=["locations"])

@router.get("/pickup-locations", response_model=list[LocationResponse])
async def get_pickup_locations(db: AsyncSession = Depends(get_db)):
    """Get all active pickup locations"""
    result = await db.execute(
        select(Location)
        .options(joinedload(Location.city))  # ← ИСПРАВЛЕНИЕ: загружаем city
        .where(Location.is_active == True)
        .order_by(Location.name)
    )
    locations = result.scalars().unique().all()  # ← ИСПРАВЛЕНИЕ: unique() для joinedload
    
    return [LocationResponse.from_orm(loc) for loc in locations]
    