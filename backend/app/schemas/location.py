from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LocationResponse(BaseModel):
    id: int
    location_id: Optional[str] = None
    name: str
    address: str
    city: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
