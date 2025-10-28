"""
Order models
Orders, order items, and receipt hash tracking
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum

from app.database import Base


class OrderStatus(str, Enum):
    """Order status enumeration"""
    DRAFT = "draft"  # В корзине
    PENDING = "pending"  # Создан, ожидает оплаты
    PAID = "paid"  # Чек загружен и валидирован
    CONFIRMED = "confirmed"  # Подтвержден менеджером
    CANCELLED = "cancelled"  # Отменен
    COMPLETED = "completed"  # Выдан клиенту


class Order(Base):
    """Order model"""
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    
    # Идентификация заказа
    order_code = Column(String(6), unique=True, nullable=False, index=True)  # 6-значный код
    qr_code_url = Column(String(500), nullable=True)  # URL QR-кода
    
    # Финансы
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="UAH")  # UAH, USD, etc.
    
    # Статус
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, index=True)
    
    # Чек
    receipt_image_url = Column(String(500), nullable=True)
    receipt_amount = Column(Numeric(10, 2), nullable=True)  # Сумма, введенная пользователем
    receipt_hash = Column(String(64), nullable=True, index=True)  # SHA-256 hash изображения
    receipt_validated_at = Column(DateTime(timezone=True), nullable=True)
    receipt_validation_result = Column(JSONB, nullable=True)  # Результат от GPT-4o
    
    # Подтверждение менеджером
    confirmed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="orders")
    location = relationship("Location", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    receipt_hash_entry = relationship("ReceiptHash", back_populates="order", uselist=False)
    
    def __repr__(self):
        return f"<Order(id={self.id}, code='{self.order_code}', status='{self.status}', total={self.total_amount})>"


class OrderItem(Base):
    """Order item model - products in an order"""
    
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    selected_options = Column(JSONB, nullable=True)  # {"size": "30см", "extras": ["Сыр", "Грибы"]}
    options_price = Column(Numeric(10, 2), default=0)
    
    total_price = Column(Numeric(10, 2), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"


class ReceiptHash(Base):
    """Receipt hash tracking - prevents duplicate receipt usage"""
    
    __tablename__ = "receipts_hash"
    
    id = Column(Integer, primary_key=True, index=True)
    image_hash = Column(String(64), unique=True, nullable=False, index=True)  # SHA-256 hash
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="receipt_hash_entry")
    
    def __repr__(self):
        return f"<ReceiptHash(id={self.id}, hash='{self.image_hash[:8]}...', order_id={self.order_id})>"
