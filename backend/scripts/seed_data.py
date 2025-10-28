"""
Script to seed the database with test data
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker, init_db
from app.models.product import Category, Product
from app.models.location import Location


async def seed_database():
    """Seed database with test data"""
    print("Starting database seeding...")
    
    await init_db()
    
    async with async_session_maker() as session:
        # Add categories
        categories = [
            Category(
                category_id="pizza",
                name="Піца",
                sort_order=1,
                is_active=True
            ),
            Category(
                category_id="drinks",
                name="Напої",
                sort_order=2,
                is_active=True
            ),
            Category(
                category_id="snacks",
                name="Закуски",
                sort_order=3,
                is_active=True
            ),
        ]
        session.add_all(categories)
        await session.commit()
        print(f"✅ Added {len(categories)} categories")
        
        # Add products
        products = [
            # Pizzas
            Product(
                product_id="margarita",
                category_id="pizza",
                name="Маргарита",
                description="Класична піца з томатами та моцарелою",
                base_price=120.0,
                options=[
                    {"type": "Розмір", "name": "Мала (25см)", "price_modifier": 0},
                    {"type": "Розмір", "name": "Середня (30см)", "price_modifier": 40},
                    {"type": "Розмір", "name": "Велика (35см)", "price_modifier": 80},
                    {"type": "Добавка", "name": "Подвійний сир", "price_modifier": 30},
                    {"type": "Добавка", "name": "Гриби", "price_modifier": 20},
                ],
                sort_order=1,
                is_active=True
            ),
            Product(
                product_id="pepperoni",
                category_id="pizza",
                name="Пепероні",
                description="Піца з пікантною салямі пепероні",
                base_price=150.0,
                options=[
                    {"type": "Розмір", "name": "Мала (25см)", "price_modifier": 0},
                    {"type": "Розмір", "name": "Середня (30см)", "price_modifier": 40},
                    {"type": "Розмір", "name": "Велика (35см)", "price_modifier": 80},
                ],
                sort_order=2,
                is_active=True
            ),
            Product(
                product_id="quattro-formaggi",
                category_id="pizza",
                name="Чотири сири",
                description="Піца з чотирма видами сиру",
                base_price=170.0,
                options=[
                    {"type": "Розмір", "name": "Мала (25см)", "price_modifier": 0},
                    {"type": "Розмір", "name": "Середня (30см)", "price_modifier": 40},
                    {"type": "Розмір", "name": "Велика (35см)", "price_modifier": 80},
                ],
                sort_order=3,
                is_active=True
            ),
            # Drinks
            Product(
                product_id="cola",
                category_id="drinks",
                name="Coca-Cola",
                description="Класична кока-кола",
                base_price=30.0,
                options=[
                    {"type": "Об'єм", "name": "0.33л", "price_modifier": 0},
                    {"type": "Об'єм", "name": "0.5л", "price_modifier": 10},
                ],
                sort_order=1,
                is_active=True
            ),
            Product(
                product_id="water",
                category_id="drinks",
                name="Вода мінеральна",
                description="Мінеральна вода",
                base_price=20.0,
                options=[
                    {"type": "Об'єм", "name": "0.5л", "price_modifier": 0},
                    {"type": "Об'єм", "name": "1л", "price_modifier": 10},
                ],
                sort_order=2,
                is_active=True
            ),
        ]
        session.add_all(products)
        await session.commit()
        print(f"✅ Added {len(products)} products")
        
        # Add locations
        locations = [
            Location(
                location_id="kyiv-center",
                city="Київ",
                name="Центральний вокзал",
                address="вул. Вокзальна, 1",
                is_active=True
            ),
            Location(
                location_id="lviv-market",
                city="Львів",
                name="Ринок Галицький",
                address="пл. Ринок, 10",
                is_active=True
            ),
            Location(
                location_id="odesa-beach",
                city="Одеса",
                name="Аркадія",
                address="Аркадія, пляж",
                is_active=True
            ),
        ]
        session.add_all(locations)
        await session.commit()
        print(f"✅ Added {len(locations)} locations")
    
    print("\n🎉 Database seeding completed successfully!")
    print("\nYou can now:")
    print("  • View categories at http://localhost:8000/api/categories")
    print("  • View products at http://localhost:8000/api/products")
    print("  • View locations at http://localhost:8000/api/pickup-locations")


if __name__ == "__main__":
    asyncio.run(seed_database())
