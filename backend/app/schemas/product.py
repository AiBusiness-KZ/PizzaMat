from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ProductResponse(BaseModel):
    id: int
    product_id: Optional[str] = None
    category_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    base_price: float
    photo_url: Optional[str] = None
    options: Optional[List[Dict[str, Any]]] = None
    is_available: bool = True
    display_order: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
