from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models.location import Location
from ..schemas.location import LocationResponse

router = APIRouter(prefix="", tags=["locations"])


@router.get("/pickup-locations", response_model=dict)
async def get_pickup_locations(db: AsyncSession = Depends(get_db)):
    """Get all active pickup locations"""
    result = await db.execute(
        select(Location)
        .where(Location.is_active == True)
        .order_by(Location.name)
    )
    locations = result.scalars().all()
    
    return {
        "success": True,
        "data": [LocationResponse.from_orm(loc) for loc in locations]
    }
