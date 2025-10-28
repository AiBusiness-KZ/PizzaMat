from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    selected_options: List[Dict[str, Any]]
    price_per_unit: float
    total_price: float


class CreateOrderRequest(BaseModel):
    user_telegram_id: Optional[str] = None
    user_telegram_name: Optional[str] = None
    order_items: List[OrderItemResponse]
    pickup_location_id: str


class OrderResponse(BaseModel):
    id: int
    order_id: str
    user_telegram_id: Optional[str] = None
    status: str
    total_amount: float
    pickup_code: str
    pickup_location_name: str
    created_at: datetime

    class Config:
        from_attributes = True
