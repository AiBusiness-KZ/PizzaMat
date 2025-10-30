from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class LocationResponse(BaseModel):
    id: int
    location_id: Optional[str] = None
    city_id: int
    name: str
    address: str
    city: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @field_validator('city', mode='before')
    @classmethod
    def extract_city_name(cls, v):
        """Extract city name from City object if needed"""
        if v is None:
            return None
        # If it's already a string, return as is
        if isinstance(v, str):
            return v
        # If it's a City object, extract the name
        if hasattr(v, 'name'):
            return v.name
        return str(v)
    
    class Config:
        from_attributes = True
