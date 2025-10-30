"""
Bot API endpoints - for Telegram bot to interact with backend
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from app.database import get_db
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.models.location import City
from app.models.bot_interaction import UserSession, BotInteraction, SupportMessage
from pydantic import BaseModel

router = APIRouter(prefix="", tags=["Bot API"])
logger = logging.getLogger(__name__)


# ==================== Pydantic Models ====================

class UserCreateRequest(BaseModel):
    telegram_id: int
    phone: str
    full_name: str
    city_id: Optional[int] = None
    language: str = "uk"


class SessionStartRequest(BaseModel):
    user_id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language: Optional[str] = None
    platform: Optional[str] = None


class InteractionLogRequest(BaseModel):
    telegram_id: int
    interaction_type: str
    session_id: Optional[int] = None
    user_id: Optional[int] = None
    command: Optional[str] = None
    message_text: Optional[str] = None
    callback_data: Optional[str] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    bot_response: Optional[str] = None
    bot_response_type: Optional[str] = None
    fsm_state: Optional[str] = None
    meta_data: Optional[dict] = None
    is_successful: bool = True
    error_message: Optional[str] = None


class SupportMessageRequest(BaseModel):
    user_id: int
    telegram_id: int
    ticket_id: str
    message_text: str
    sender_type: str = "user"
    message_type: str = "text"
    file_url: Optional[str] = None
    order_id: Optional[int] = None
    thread_id: Optional[str] = None


# ==================== User Endpoints ====================

@router.get("/users/{telegram_id}")
async def get_user_by_telegram_id(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Get user by Telegram ID"""
    query = select(User).where(User.telegram_id == telegram_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "phone": user.phone,
        "full_name": user.full_name,
        "city_id": user.city_id,
        "language": user.language,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat()
    }


@router.post("/users")
async def create_user(request: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    """Create new user"""
    # Check if user already exists
    existing_query = select(User).where(User.telegram_id == request.telegram_id)
    existing_result = await db.execute(existing_query)
    existing_user = existing_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user
    user = User(
        telegram_id=request.telegram_id,
        phone=request.phone,
        full_name=request.full_name,
        city_id=request.city_id,
        language=request.language
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "phone": user.phone,
        "full_name": user.full_name,
        "city_id": user.city_id,
        "language": user.language,
        "created_at": user.created_at.isoformat()
    }


@router.get("/cities")
async def get_cities(db: AsyncSession = Depends(get_db)):
    """Get all active cities"""
    query = select(City).where(City.is_active == True).order_by(City.name)
    result = await db.execute(query)
    cities = result.scalars().all()

    return [
        {
            "id": city.id,
            "name": city.name,
            "is_active": city.is_active
        }
        for city in cities
    ]


# ==================== Order Endpoints ====================

@router.get("/orders/user/{telegram_id}")
async def get_user_orders(
    telegram_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get user's orders"""
    # Get user
    user_query = select(User).where(User.telegram_id == telegram_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get orders
    orders_query = select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc()).limit(limit)
    orders_result = await db.execute(orders_query)
    orders = orders_result.scalars().all()

    return [
        {
            "id": order.id,
            "order_code": order.order_code,
            "status": order.status.value,
            "total_amount": float(order.total_amount),
            "created_at": order.created_at.isoformat()
        }
        for order in orders
    ]


@router.get("/orders/{order_id}")
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """Get order by ID"""
    query = select(Order).where(Order.id == order_id)
    result = await db.execute(query)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "order_code": order.order_code,
        "status": order.status.value,
        "total_amount": float(order.total_amount),
        "receipt_image_url": order.receipt_image_url,
        "created_at": order.created_at.isoformat(),
        "user": {
            "telegram_id": order.user.telegram_id,
            "full_name": order.user.full_name
        },
        "location": {
            "name": order.location.name,
            "address": order.location.address,
            "working_hours": order.location.working_hours
        }
    }


# ==================== Logging Endpoints ====================

@router.post("/sessions")
async def log_session_start(request: SessionStartRequest, db: AsyncSession = Depends(get_db)):
    """Log session start"""
    session = UserSession(
        user_id=request.user_id,
        telegram_id=request.telegram_id,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        language=request.language,
        platform=request.platform
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {
        "id": session.id,
        "session_start": session.session_start.isoformat()
    }


@router.put("/sessions/{session_id}/end")
async def log_session_end(session_id: int, db: AsyncSession = Depends(get_db)):
    """Log session end"""
    query = select(UserSession).where(UserSession.id == session_id)
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.session_end = datetime.utcnow()
    session.duration_seconds = int((session.session_end - session.session_start).total_seconds())

    await db.commit()

    return {"status": "ok"}


@router.post("/interactions")
async def log_interaction(request: InteractionLogRequest, db: AsyncSession = Depends(get_db)):
    """Log bot interaction"""
    interaction = BotInteraction(
        telegram_id=request.telegram_id,
        interaction_type=request.interaction_type,
        session_id=request.session_id,
        user_id=request.user_id,
        command=request.command,
        message_text=request.message_text,
        callback_data=request.callback_data,
        chat_id=request.chat_id,
        message_id=request.message_id,
        bot_response=request.bot_response,
        bot_response_type=request.bot_response_type,
        fsm_state=request.fsm_state,
        meta_data=request.meta_data,
        is_successful=request.is_successful,
        error_message=request.error_message
    )

    db.add(interaction)
    await db.commit()
    await db.refresh(interaction)

    return {"id": interaction.id, "created_at": interaction.created_at.isoformat()}


@router.post("/support")
async def create_support_message(request: SupportMessageRequest, db: AsyncSession = Depends(get_db)):
    """Create support message"""
    message = SupportMessage(
        user_id=request.user_id,
        telegram_id=request.telegram_id,
        ticket_id=request.ticket_id,
        message_text=request.message_text,
        sender_type=request.sender_type,
        message_type=request.message_type,
        file_url=request.file_url,
        order_id=request.order_id,
        thread_id=request.thread_id
    )

    db.add(message)
    await db.commit()
    await db.refresh(message)

    return {
        "id": message.id,
        "ticket_id": message.ticket_id,
        "created_at": message.created_at.isoformat()
    }
