"""
Analytics and statistics endpoints for manager dashboard
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from app.database import get_db
from app.models.bot_interaction import UserSession, BotInteraction, SupportMessage, BotStatistics
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.core.dependencies import get_admin_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)


@router.get("/dashboard")
async def get_dashboard_stats(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_admin_user)  # Uncomment when auth is enabled
):
    """
    Get aggregated dashboard statistics for last N days
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    # Total users
    total_users_query = select(func.count(User.id))
    total_users_result = await db.execute(total_users_query)
    total_users = total_users_result.scalar()

    # New users in period
    new_users_query = select(func.count(User.id)).where(User.created_at >= start_date)
    new_users_result = await db.execute(new_users_query)
    new_users = new_users_result.scalar()

    # Active users (had sessions in period)
    active_users_query = select(func.count(func.distinct(UserSession.user_id))).where(
        UserSession.session_start >= start_date
    )
    active_users_result = await db.execute(active_users_query)
    active_users = active_users_result.scalar()

    # Total sessions
    total_sessions_query = select(func.count(UserSession.id)).where(
        UserSession.session_start >= start_date
    )
    total_sessions_result = await db.execute(total_sessions_query)
    total_sessions = total_sessions_result.scalar()

    # Avg session duration
    avg_duration_query = select(func.avg(UserSession.duration_seconds)).where(
        and_(
            UserSession.session_start >= start_date,
            UserSession.duration_seconds.isnot(None)
        )
    )
    avg_duration_result = await db.execute(avg_duration_query)
    avg_duration = avg_duration_result.scalar() or 0

    # Orders statistics
    orders_created_query = select(func.count(Order.id)).where(Order.created_at >= start_date)
    orders_created_result = await db.execute(orders_created_query)
    orders_created = orders_created_result.scalar()

    orders_paid_query = select(func.count(Order.id)).where(
        and_(Order.created_at >= start_date, Order.status == OrderStatus.PAID)
    )
    orders_paid_result = await db.execute(orders_paid_query)
    orders_paid = orders_paid_result.scalar()

    orders_completed_query = select(func.count(Order.id)).where(
        and_(Order.created_at >= start_date, Order.status == OrderStatus.COMPLETED)
    )
    orders_completed_result = await db.execute(orders_completed_query)
    orders_completed = orders_completed_result.scalar()

    orders_cancelled_query = select(func.count(Order.id)).where(
        and_(Order.created_at >= start_date, Order.status == OrderStatus.CANCELLED)
    )
    orders_cancelled_result = await db.execute(orders_cancelled_query)
    orders_cancelled = orders_cancelled_result.scalar()

    # Revenue
    revenue_query = select(func.sum(Order.total_amount)).where(
        and_(
            Order.created_at >= start_date,
            Order.status.in_([OrderStatus.COMPLETED, OrderStatus.CONFIRMED, OrderStatus.PAID])
        )
    )
    revenue_result = await db.execute(revenue_query)
    total_revenue = float(revenue_result.scalar() or 0)

    # Support tickets
    support_opened_query = select(func.count(SupportMessage.id)).where(
        and_(
            SupportMessage.created_at >= start_date,
            SupportMessage.sender_type == "user"
        )
    )
    support_opened_result = await db.execute(support_opened_query)
    support_opened = support_opened_result.scalar()

    support_closed_query = select(func.count(func.distinct(SupportMessage.ticket_id))).where(
        and_(
            SupportMessage.created_at >= start_date,
            SupportMessage.status == "closed"
        )
    )
    support_closed_result = await db.execute(support_closed_query)
    support_closed = support_closed_result.scalar()

    # Top commands
    top_commands_query = select(
        BotInteraction.command,
        func.count(BotInteraction.id).label('count')
    ).where(
        and_(
            BotInteraction.created_at >= start_date,
            BotInteraction.command.isnot(None)
        )
    ).group_by(BotInteraction.command).order_by(desc('count')).limit(10)

    top_commands_result = await db.execute(top_commands_query)
    top_commands = {row.command: row.count for row in top_commands_result}

    # Conversion funnel
    menu_views_query = select(func.count(BotInteraction.id)).where(
        and_(
            BotInteraction.created_at >= start_date,
            BotInteraction.command == "/menu"
        )
    )
    menu_views_result = await db.execute(menu_views_query)
    menu_views = menu_views_result.scalar()

    return {
        "period_days": days,
        "start_date": start_date.isoformat(),
        "users": {
            "total": total_users,
            "new": new_users,
            "active": active_users
        },
        "sessions": {
            "total": total_sessions,
            "avg_duration_seconds": int(avg_duration)
        },
        "orders": {
            "created": orders_created,
            "paid": orders_paid,
            "completed": orders_completed,
            "cancelled": orders_cancelled,
            "conversion_rate": round((orders_completed / orders_created * 100) if orders_created > 0 else 0, 2)
        },
        "revenue": {
            "total": total_revenue,
            "avg_order_value": round(total_revenue / orders_completed if orders_completed > 0 else 0, 2)
        },
        "support": {
            "tickets_opened": support_opened,
            "tickets_closed": support_closed
        },
        "engagement": {
            "menu_views": menu_views,
            "top_commands": top_commands
        }
    }


@router.get("/interactions")
async def get_user_interactions(
    user_id: Optional[int] = None,
    telegram_id: Optional[int] = None,
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_admin_user)
):
    """
    Get detailed interaction history for a user or all users
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    query = select(BotInteraction).where(BotInteraction.created_at >= start_date)

    if user_id:
        query = query.where(BotInteraction.user_id == user_id)
    if telegram_id:
        query = query.where(BotInteraction.telegram_id == telegram_id)

    query = query.order_by(desc(BotInteraction.created_at)).limit(limit)

    result = await db.execute(query)
    interactions = result.scalars().all()

    return {
        "count": len(interactions),
        "interactions": [
            {
                "id": interaction.id,
                "timestamp": interaction.created_at.isoformat(),
                "user_id": interaction.user_id,
                "telegram_id": interaction.telegram_id,
                "type": interaction.interaction_type,
                "command": interaction.command,
                "message_text": interaction.message_text,
                "callback_data": interaction.callback_data,
                "bot_response": interaction.bot_response,
                "fsm_state": interaction.fsm_state,
                "is_successful": interaction.is_successful,
                "error_message": interaction.error_message
            }
            for interaction in interactions
        ]
    }


@router.get("/sessions")
async def get_user_sessions(
    user_id: Optional[int] = None,
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_admin_user)
):
    """
    Get user sessions with metrics
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    query = select(UserSession).where(UserSession.session_start >= start_date)

    if user_id:
        query = query.where(UserSession.user_id == user_id)

    query = query.order_by(desc(UserSession.session_start)).limit(100)

    result = await db.execute(query)
    sessions = result.scalars().all()

    return {
        "count": len(sessions),
        "sessions": [
            {
                "id": session.id,
                "user_id": session.user_id,
                "telegram_id": session.telegram_id,
                "session_start": session.session_start.isoformat(),
                "session_end": session.session_end.isoformat() if session.session_end else None,
                "duration_seconds": session.duration_seconds,
                "messages_sent": session.messages_sent,
                "commands_used": session.commands_used,
                "buttons_clicked": session.buttons_clicked,
                "platform": session.platform,
                "user_info": {
                    "username": session.username,
                    "first_name": session.first_name,
                    "last_name": session.last_name,
                    "language": session.language
                }
            }
            for session in sessions
        ]
    }


@router.get("/support-messages")
async def get_support_messages(
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    days: int = Query(30, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_admin_user)
):
    """
    Get support/feedback messages for manager review
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    query = select(SupportMessage).where(SupportMessage.created_at >= start_date)

    if status:
        query = query.where(SupportMessage.status == status)
    if user_id:
        query = query.where(SupportMessage.user_id == user_id)

    query = query.order_by(desc(SupportMessage.created_at)).limit(100)

    result = await db.execute(query)
    messages = result.scalars().all()

    return {
        "count": len(messages),
        "messages": [
            {
                "id": msg.id,
                "ticket_id": msg.ticket_id,
                "user_id": msg.user_id,
                "telegram_id": msg.telegram_id,
                "status": msg.status,
                "sender_type": msg.sender_type,
                "sender_name": msg.sender_name,
                "message_text": msg.message_text,
                "message_type": msg.message_type,
                "file_url": msg.file_url,
                "order_id": msg.order_id,
                "thread_id": msg.thread_id,
                "created_at": msg.created_at.isoformat(),
                "responded_at": msg.responded_at.isoformat() if msg.responded_at else None,
                "response_time_seconds": msg.response_time_seconds
            }
            for msg in messages
        ]
    }


@router.get("/user-journey/{telegram_id}")
async def get_user_journey(
    telegram_id: int,
    days: int = Query(30, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_admin_user)
):
    """
    Get complete user journey: sessions, interactions, orders, support messages
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    # Get user
    user_query = select(User).where(User.telegram_id == telegram_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get sessions
    sessions_query = select(UserSession).where(
        and_(
            UserSession.telegram_id == telegram_id,
            UserSession.session_start >= start_date
        )
    ).order_by(desc(UserSession.session_start))
    sessions_result = await db.execute(sessions_query)
    sessions = sessions_result.scalars().all()

    # Get interactions
    interactions_query = select(BotInteraction).where(
        and_(
            BotInteraction.telegram_id == telegram_id,
            BotInteraction.created_at >= start_date
        )
    ).order_by(desc(BotInteraction.created_at)).limit(200)
    interactions_result = await db.execute(interactions_query)
    interactions = interactions_result.scalars().all()

    # Get orders
    orders_query = select(Order).where(
        and_(
            Order.user_id == user.id,
            Order.created_at >= start_date
        )
    ).order_by(desc(Order.created_at))
    orders_result = await db.execute(orders_query)
    orders = orders_result.scalars().all()

    # Get support messages
    support_query = select(SupportMessage).where(
        and_(
            SupportMessage.telegram_id == telegram_id,
            SupportMessage.created_at >= start_date
        )
    ).order_by(desc(SupportMessage.created_at))
    support_result = await db.execute(support_query)
    support_messages = support_result.scalars().all()

    return {
        "user": {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "phone": user.phone,
            "full_name": user.full_name,
            "language": user.language,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        },
        "sessions": [
            {
                "id": s.id,
                "start": s.session_start.isoformat(),
                "end": s.session_end.isoformat() if s.session_end else None,
                "duration": s.duration_seconds,
                "messages": s.messages_sent,
                "commands": s.commands_used,
                "buttons": s.buttons_clicked
            }
            for s in sessions
        ],
        "interactions": [
            {
                "timestamp": i.created_at.isoformat(),
                "type": i.interaction_type,
                "command": i.command,
                "text": i.message_text,
                "response": i.bot_response
            }
            for i in interactions
        ],
        "orders": [
            {
                "id": o.id,
                "code": o.order_code,
                "status": o.status.value,
                "amount": float(o.total_amount),
                "created_at": o.created_at.isoformat()
            }
            for o in orders
        ],
        "support_messages": [
            {
                "ticket_id": sm.ticket_id,
                "sender": sm.sender_type,
                "text": sm.message_text,
                "created_at": sm.created_at.isoformat()
            }
            for sm in support_messages
        ],
        "summary": {
            "total_sessions": len(sessions),
            "total_interactions": len(interactions),
            "total_orders": len(orders),
            "total_support_tickets": len(set(sm.ticket_id for sm in support_messages)),
            "avg_session_duration": sum(s.duration_seconds or 0 for s in sessions) // len(sessions) if sessions else 0
        }
    }


@router.get("/daily-stats")
async def get_daily_statistics(
    days: int = Query(30, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_admin_user)
):
    """
    Get daily aggregated statistics for charts
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    query = select(BotStatistics).where(
        BotStatistics.date >= start_date
    ).order_by(BotStatistics.date)

    result = await db.execute(query)
    stats = result.scalars().all()

    return {
        "count": len(stats),
        "stats": [
            {
                "date": stat.date.isoformat(),
                "users": {
                    "total": stat.total_users,
                    "new": stat.new_users,
                    "active": stat.active_users
                },
                "sessions": {
                    "total": stat.total_sessions,
                    "avg_duration": stat.avg_session_duration
                },
                "interactions": {
                    "total": stat.total_interactions,
                    "commands": stat.total_commands,
                    "messages": stat.total_messages,
                    "callbacks": stat.total_callbacks
                },
                "orders": {
                    "created": stat.orders_created,
                    "paid": stat.orders_paid,
                    "confirmed": stat.orders_confirmed,
                    "completed": stat.orders_completed,
                    "cancelled": stat.orders_cancelled
                },
                "revenue": {
                    "total": stat.total_revenue / 100,  # Convert from kopecks
                    "avg_order": stat.avg_order_value / 100
                },
                "support": {
                    "opened": stat.support_tickets_opened,
                    "closed": stat.support_tickets_closed,
                    "avg_response_time": stat.avg_response_time
                },
                "funnel": {
                    "menu_views": stat.menu_views,
                    "cart_additions": stat.cart_additions,
                    "checkout_started": stat.checkout_started,
                    "receipt_uploaded": stat.receipt_uploaded
                }
            }
            for stat in stats
        ]
    }
