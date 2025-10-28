from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CategoryResponse(BaseModel):
    id: int
    category_id: Optional[str] = None
    name: str
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
