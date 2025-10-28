"""
Admin API routes
CRUD operations for categories, products, locations, settings, orders
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from typing import List, Optional
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.models.product import Category, Product, ProductOption
from app.models.location import City, Location
from app.models.order import Order, OrderItem
from app.models.settings import SiteSettings
from app.config import settings
from app.core.dependencies import get_admin_user
from app.core.file_validation import validate_upload_image, FileValidator

router = APIRouter(
    prefix="/api/admin", 
    tags=["admin"],
    dependencies=[Depends(get_admin_user)]
)


# ===== CATEGORIES =====

@router.get("/categories")
async def get_categories_admin(db: AsyncSession = Depends(get_db)):
    """Get all categories (including inactive)"""
    result = await db.execute(select(Category).order_by(Category.sort_order))
    categories = result.scalars().all()
    return {
        "success": True,
        "data": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "sort_order": c.sort_order,
                "is_active": c.is_active,
                "created_at": c.created_at.isoformat(),
            }
            for c in categories
        ]
    }


@router.post("/categories")
async def create_category(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    sort_order: int = Form(0),
    is_active: bool = Form(True),
    db: AsyncSession = Depends(get_db)
):
    """Create new category"""
    category = Category(
        name=name,
        description=description,
        sort_order=sort_order,
        is_active=is_active
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return {"success": True, "data": {"id": category.id, "name": category.name}}


@router.put("/categories/{category_id}")
async def update_category(
    category_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    sort_order: int = Form(0),
    is_active: bool = Form(True),
    db: AsyncSession = Depends(get_db)
):
    """Update category"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = name
    category.description = description
    category.sort_order = sort_order
    category.is_active = is_active
    
    await db.commit()
    return {"success": True, "message": "Category updated"}


@router.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Delete category"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await db.delete(category)
    await db.commit()
    return {"success": True, "message": "Category deleted"}


# ===== PRODUCTS =====

@router.get("/products")
async def get_products_admin(db: AsyncSession = Depends(get_db)):
    """Get all products (including inactive)"""
    result = await db.execute(
        select(Product).order_by(Product.category_id, Product.sort_order)
    )
    products = result.scalars().all()
    
    return {
        "success": True,
        "data": [
            {
                "id": p.id,
                "category_id": p.category_id,
                "name": p.name,
                "description": p.description,
                "base_price": float(p.base_price),
                "image_url": p.image_url,
                "is_active": p.is_active,
                "sort_order": p.sort_order,
                "created_at": p.created_at.isoformat(),
            }
            for p in products
        ]
    }


@router.post("/products")
async def create_product(
    category_id: int = Form(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    base_price: float = Form(...),
    sort_order: int = Form(0),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Create new product"""
    # Validate base_price
    if base_price < 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    
    image_url = None
    if image:
        # Validate image
        await validate_upload_image(image)
        
        # Save uploaded image
        ext = os.path.splitext(image.filename)[1]
        filename = f"product_{uuid.uuid4()}{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            content = await image.read()
            f.write(content)
        
        image_url = f"/uploads/{filename}"
    
    product = Product(
        category_id=category_id,
        name=name,
        description=description,
        base_price=base_price,
        image_url=image_url,
        is_active=is_active,
        sort_order=sort_order
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    return {"success": True, "data": {"id": product.id, "name": product.name}}


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    category_id: int = Form(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    base_price: float = Form(...),
    sort_order: int = Form(0),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Update product"""
    # Validate base_price
    if base_price < 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update image if provided
    if image:
        # Validate image
        await validate_upload_image(image)
        
        ext = os.path.splitext(image.filename)[1]
        filename = f"product_{uuid.uuid4()}{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            content = await image.read()
            f.write(content)
        
        product.image_url = f"/uploads/{filename}"
    
    product.category_id = category_id
    product.name = name
    product.description = description
    product.base_price = base_price
    product.sort_order = sort_order
    product.is_active = is_active
    
    await db.commit()
    return {"success": True, "message": "Product updated"}


@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Delete product"""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await db.delete(product)
    await db.commit()
    return {"success": True, "message": "Product deleted"}


# ===== LOCATIONS =====

@router.get("/locations")
async def get_locations_admin(db: AsyncSession = Depends(get_db)):
    """Get all locations"""
    result = await db.execute(
        select(Location, City)
        .join(City)
        .order_by(City.name, Location.name)
    )
    locations = result.all()
    
    return {
        "success": True,
        "data": [
            {
                "id": loc.id,
                "city_id": loc.city_id,
                "city_name": city.name,
                "name": loc.name,
                "address": loc.address,
                "working_hours": loc.working_hours,
                "is_active": loc.is_active,
            }
            for loc, city in locations
        ]
    }


@router.post("/locations")
async def create_location(
    city_id: int = Form(...),
    name: str = Form(...),
    address: str = Form(...),
    working_hours: Optional[str] = Form(None),
    is_active: bool = Form(True),
    db: AsyncSession = Depends(get_db)
):
    """Create new location"""
    location = Location(
        city_id=city_id,
        name=name,
        address=address,
        working_hours=working_hours,
        is_active=is_active
    )
    db.add(location)
    await db.commit()
    await db.refresh(location)
    return {"success": True, "data": {"id": location.id, "name": location.name}}


@router.put("/locations/{location_id}")
async def update_location(
    location_id: int,
    city_id: int = Form(...),
    name: str = Form(...),
    address: str = Form(...),
    working_hours: Optional[str] = Form(None),
    is_active: bool = Form(True),
    db: AsyncSession = Depends(get_db)
):
    """Update location"""
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    location.city_id = city_id
    location.name = name
    location.address = address
    location.working_hours = working_hours
    location.is_active = is_active
    
    await db.commit()
    return {"success": True, "message": "Location updated"}


@router.delete("/locations/{location_id}")
async def delete_location(location_id: int, db: AsyncSession = Depends(get_db)):
    """Delete location"""
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    await db.delete(location)
    await db.commit()
    return {"success": True, "message": "Location deleted"}


# ===== CITIES =====

@router.get("/cities")
async def get_cities(db: AsyncSession = Depends(get_db)):
    """Get all cities"""
    result = await db.execute(select(City).order_by(City.name))
    cities = result.scalars().all()
    return {
        "success": True,
        "data": [{"id": c.id, "name": c.name, "is_active": c.is_active} for c in cities]
    }


@router.post("/cities")
async def create_city(
    name: str = Form(...),
    is_active: bool = Form(True),
    db: AsyncSession = Depends(get_db)
):
    """Create new city"""
    city = City(name=name, is_active=is_active)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return {"success": True, "data": {"id": city.id, "name": city.name}}


# ===== SETTINGS =====

@router.get("/settings")
async def get_settings(db: AsyncSession = Depends(get_db)):
    """Get site settings"""
    result = await db.execute(select(SiteSettings).where(SiteSettings.id == 1))
    settings_obj = result.scalar_one_or_none()
    
    if not settings_obj:
        # Create default settings
        settings_obj = SiteSettings(id=1, site_name="PizzaMat")
        db.add(settings_obj)
        await db.commit()
        await db.refresh(settings_obj)
    
    return {
        "success": True,
        "data": {
            "id": settings_obj.id,
            "site_name": settings_obj.site_name,
            "site_logo": settings_obj.site_logo,
            "site_description": settings_obj.site_description,
            "phone": settings_obj.phone,
            "email": settings_obj.email,
            "address": settings_obj.address,
            "bot_token": settings_obj.bot_token,
            "manager_channel_id": settings_obj.manager_channel_id,
            "admin_telegram_ids": settings_obj.admin_telegram_ids,
            "openai_api_key": settings_obj.openai_api_key,
            "n8n_url": settings_obj.n8n_url,
            "n8n_webhook_secret": settings_obj.n8n_webhook_secret,
            "extra_settings": settings_obj.extra_settings,
            "updated_at": settings_obj.updated_at.isoformat() if settings_obj.updated_at else None,
        }
    }


@router.put("/settings")
async def update_settings(
    site_name: Optional[str] = Form(None),
    site_description: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    bot_token: Optional[str] = Form(None),
    manager_channel_id: Optional[str] = Form(None),
    admin_telegram_ids: Optional[str] = Form(None),
    openai_api_key: Optional[str] = Form(None),
    n8n_url: Optional[str] = Form(None),
    n8n_webhook_secret: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Update site settings"""
    result = await db.execute(select(SiteSettings).where(SiteSettings.id == 1))
    settings_obj = result.scalar_one_or_none()
    
    if not settings_obj:
        settings_obj = SiteSettings(id=1)
        db.add(settings_obj)
    
    # Update logo if provided
    if logo:
        # Validate logo
        await validate_upload_image(logo)
        
        ext = os.path.splitext(logo.filename)[1]
        filename = f"logo_{uuid.uuid4()}{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as f:
            content = await logo.read()
            f.write(content)
        
        settings_obj.site_logo = f"/uploads/{filename}"
    
    if site_name: settings_obj.site_name = site_name
    if site_description: settings_obj.site_description = site_description
    if phone: settings_obj.phone = phone
    if email: settings_obj.email = email
    if address: settings_obj.address = address
    if bot_token: settings_obj.bot_token = bot_token
    if manager_channel_id: settings_obj.manager_channel_id = manager_channel_id
    if admin_telegram_ids: settings_obj.admin_telegram_ids = admin_telegram_ids
    if openai_api_key: settings_obj.openai_api_key = openai_api_key
    if n8n_url: settings_obj.n8n_url = n8n_url
    if n8n_webhook_secret: settings_obj.n8n_webhook_secret = n8n_webhook_secret
    
    await db.commit()
    return {"success": True, "message": "Settings updated"}


# ===== ORDERS =====

@router.get("/orders")
async def get_orders_admin(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get all orders with filters"""
    query = select(Order).order_by(Order.created_at.desc())
    
    if status:
        query = query.where(Order.status == status)
    
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    orders = result.scalars().all()
    
    return {
        "success": True,
        "data": [
            {
                "id": o.id,
                "order_id": o.order_id,
                "user_telegram_id": o.user_telegram_id,
                "status": o.status.value if hasattr(o.status, 'value') else o.status,
                "total_amount": float(o.total_amount),
                "pickup_code": o.pickup_code,
                "location_id": o.location_id,
                "created_at": o.created_at.isoformat(),
            }
            for o in orders
        ]
    }


@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Update order status"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    await db.commit()
    return {"success": True, "message": "Order status updated"}


# ===== FILE UPLOAD =====

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file"""
    # Validate image
    await validate_upload_image(file)
    
    ext = os.path.splitext(file.filename)[1]
    filename = f"upload_{uuid.uuid4()}{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "success": True,
        "data": {
            "url": f"/uploads/{filename}",
            "filename": filename
        }
    }
