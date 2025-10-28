"""
Product models
Categories, products, options, and location-product relationships
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class Category(Base):
    """Product category model"""
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0, index=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Product(Base):
    """Product model - base catalog"""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    sort_order = Column(Integer, default=0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    options = relationship("ProductOption", back_populates="product", cascade="all, delete-orphan")
    location_products = relationship("LocationProduct", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', base_price={self.base_price})>"


class ProductOption(Base):
    """Product option model (sizes, extras, etc.)"""
    
    __tablename__ = "product_options"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    option_name = Column(String(100), nullable=False)  # 'size', 'extra', etc.
    option_value = Column(String(100), nullable=False)  # '25см', 'Сыр', etc.
    price_modifier = Column(Numeric(10, 2), default=0)  # +500, +200, etc.
    is_active = Column(Boolean, default=True, index=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="options")
    
    def __repr__(self):
        return f"<ProductOption(id={self.id}, name='{self.option_name}', value='{self.option_value}')>"


class LocationProduct(Base):
    """Location-Product relationship - controls what products are available at each location"""
    
    __tablename__ = "location_products"
    __table_args__ = (
        UniqueConstraint('location_id', 'product_id', name='uq_location_product'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    price_override = Column(Numeric(10, 2), nullable=True)  # NULL = use base_price
    is_available = Column(Boolean, default=True, index=True)
    stock_quantity = Column(Integer, nullable=True)  # NULL = unlimited
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    location = relationship("Location", back_populates="location_products")
    product = relationship("Product", back_populates="location_products")
    
    def __repr__(self):
        return f"<LocationProduct(location_id={self.location_id}, product_id={self.product_id})>"
