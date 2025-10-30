from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..database import get_db
from ..models.product import Category, Product
from ..schemas.category import CategoryResponse
from ..schemas.product import ProductResponse

router = APIRouter(prefix="", tags=["menu"])


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all active categories"""
    result = await db.execute(
        select(Category)
        .where(Category.is_active == True)
        .order_by(Category.sort_order)
    )
    categories = result.scalars().all()
    
    return {
        "success": True,
        "data": [CategoryResponse.from_orm(cat).dict() for cat in categories]
    }


@router.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    """Get all available products"""
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.sort_order)
    )
    products = result.scalars().all()
    
    # Manual mapping - read all attributes while in session context
    products_data = []
    for prod in products:
        # Force load all attributes within session context
        prod_id = prod.id
        prod_cat_id = prod.category_id  
        prod_name = prod.name
        prod_desc = prod.description
        prod_price = prod.base_price
        prod_active = prod.is_active
        prod_sort = prod.sort_order
        prod_created = prod.created_at
        prod_updated = prod.updated_at
        
        # Try to get optional fields
        try:
            prod_product_id = prod.product_id if hasattr(prod, 'product_id') else None
        except:
            prod_product_id = None
            
        try:
            prod_image = prod.image_url if hasattr(prod, 'image_url') else None
        except:
            prod_image = None
            
        try:
            prod_options = prod.options if hasattr(prod, 'options') else None
        except:
            prod_options = None
        
        products_data.append({
            "id": prod_id,
            "product_id": prod_product_id,
            "category_id": prod_cat_id,
            "name": prod_name,
            "description": prod_desc,
            "base_price": float(prod_price),
            "photo_url": prod_image,
            "options": prod_options,
            "is_available": prod_active,
            "display_order": prod_sort or 0,
            "created_at": prod_created,
            "updated_at": prod_updated,
        })
    
    return {
        "success": True,
        "data": products_data
    }
