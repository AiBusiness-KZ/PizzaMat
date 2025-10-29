"""
Bot interaction models for tracking and analytics
Tracks all user interactions with the Telegram bot
"""

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class UserSession(Base):
    """User session tracking - when user starts/stops interacting with bot"""

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    telegram_id = Column(BigInteger, nullable=False, index=True)

    # Session info
    session_start = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    session_end = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)  # Calculated on session end

    # User context
    language = Column(String(5), nullable=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)

    # Metrics
    messages_sent = Column(Integer, default=0)
    commands_used = Column(Integer, default=0)
    buttons_clicked = Column(Integer, default=0)

    # Platform info
    platform = Column(String(50), nullable=True)  # ios, android, web, desktop

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", backref="sessions")
    interactions = relationship("BotInteraction", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, start={self.session_start})>"


class BotInteraction(Base):
    """Detailed interaction logging - every message, command, button click"""

    __tablename__ = "bot_interactions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    telegram_id = Column(BigInteger, nullable=False, index=True)

    # Interaction type
    interaction_type = Column(String(50), nullable=False, index=True)
    # Types: 'command', 'message', 'callback_query', 'inline_query', 'webapp_data', 'photo', 'document'

    # Content
    command = Column(String(100), nullable=True, index=True)  # /start, /menu, etc.
    message_text = Column(Text, nullable=True)
    callback_data = Column(String(255), nullable=True)

    # Context
    chat_id = Column(BigInteger, nullable=False)
    message_id = Column(Integer, nullable=True)

    # Bot response
    bot_response = Column(Text, nullable=True)
    bot_response_type = Column(String(50), nullable=True)  # 'text', 'photo', 'keyboard', 'webapp'

    # State info
    fsm_state = Column(String(100), nullable=True)  # Current FSM state

    # Additional data
    metadata = Column(JSONB, nullable=True)  # Any extra data: buttons clicked, webapp data, etc.

    # Success/Error tracking
    is_successful = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    session = relationship("UserSession", back_populates="interactions")
    user = relationship("User", backref="interactions")

    def __repr__(self):
        return f"<BotInteraction(id={self.id}, type='{self.interaction_type}', user_id={self.user_id})>"


class SupportMessage(Base):
    """Support/feedback messages between users and managers"""

    __tablename__ = "support_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    telegram_id = Column(BigInteger, nullable=False, index=True)

    # Ticket info
    ticket_id = Column(String(20), unique=True, nullable=False, index=True)  # Format: SUPPORT-XXXXXX
    status = Column(String(20), default="open", index=True)  # open, in_progress, closed

    # Message content
    sender_type = Column(String(20), nullable=False)  # 'user' or 'manager'
    sender_telegram_id = Column(BigInteger, nullable=True)  # If manager responds
    sender_name = Column(String(255), nullable=True)

    message_text = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, photo, document
    file_url = Column(String(500), nullable=True)  # If photo/document attached

    # Related order (optional)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)

    # Thread tracking
    parent_message_id = Column(Integer, ForeignKey("support_messages.id"), nullable=True)
    thread_id = Column(String(20), nullable=True, index=True)  # Groups messages in conversation

    # Manager response tracking
    responded_at = Column(DateTime(timezone=True), nullable=True)
    response_time_seconds = Column(Integer, nullable=True)  # Time to first response

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", backref="support_messages")
    order = relationship("Order", backref="support_messages")
    parent = relationship("SupportMessage", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<SupportMessage(id={self.id}, ticket='{self.ticket_id}', from='{self.sender_type}')>"


class BotStatistics(Base):
    """Aggregated daily statistics for dashboard"""

    __tablename__ = "bot_statistics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False, unique=True, index=True)

    # User metrics
    total_users = Column(Integer, default=0)
    new_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)  # Users who interacted today

    # Session metrics
    total_sessions = Column(Integer, default=0)
    avg_session_duration = Column(Integer, default=0)  # Seconds

    # Interaction metrics
    total_interactions = Column(Integer, default=0)
    total_commands = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    total_callbacks = Column(Integer, default=0)

    # Order metrics
    orders_created = Column(Integer, default=0)
    orders_paid = Column(Integer, default=0)
    orders_confirmed = Column(Integer, default=0)
    orders_cancelled = Column(Integer, default=0)
    orders_completed = Column(Integer, default=0)

    # Revenue metrics
    total_revenue = Column(Integer, default=0)  # In kopecks/cents
    avg_order_value = Column(Integer, default=0)

    # Support metrics
    support_tickets_opened = Column(Integer, default=0)
    support_tickets_closed = Column(Integer, default=0)
    avg_response_time = Column(Integer, default=0)  # Seconds

    # Conversion funnel
    menu_views = Column(Integer, default=0)
    cart_additions = Column(Integer, default=0)
    checkout_started = Column(Integer, default=0)
    receipt_uploaded = Column(Integer, default=0)

    # Popular commands
    top_commands = Column(JSONB, nullable=True)  # {"/menu": 150, "/orders": 80, ...}

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<BotStatistics(date={self.date}, active_users={self.active_users})>"
