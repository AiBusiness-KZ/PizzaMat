"""
Simplified seed script - add test data directly
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import async_session_maker


async def seed_database():
    """Seed database with test data using raw SQL"""
    print("Starting database seeding...")
    
    async with async_session_maker() as session:
        # Clear existing data
        await session.execute(text("TRUNCATE categories, products, locations RESTART IDENTITY CASCADE"))
        
        # Add categories
        await session.execute(text("""
            INSERT INTO categories (category_id, name, sort_order, is_active) VALUES
            ('pizza', 'Піца', 1, true),
            ('drinks', 'Напої', 2, true),
            ('snacks', 'Закуски', 3, true)
        """))
        print("✅ Added categories")
        
        # Add products
        await session.execute(text("""
            INSERT INTO products (product_id, category_id, name, description, base_price, options, sort_order, is_active) VALUES
            ('margarita', 'pizza', 'Маргарита', 'Класична піца з томатами та моцарелою', 120.0, 
             '[{"type": "Розмір", "name": "Мала (25см)", "price_modifier": 0}, 
               {"type": "Розмір", "name": "Середня (30см)", "price_modifier": 40},
               {"type": "Розмір", "name": "Велика (35см)", "price_modifier": 80},
               {"type": "Добавка", "name": "Подвійний сир", "price_modifier": 30}]'::jsonb, 
             1, true),
            ('pepperoni', 'pizza', 'Пепероні', 'Піца з пікантною салямі пепероні', 150.0,
             '[{"type": "Розмір", "name": "Мала (25см)", "price_modifier": 0},
               {"type": "Розмір", "name": "Середня (30см)", "price_modifier": 40},
               {"type": "Розмір", "name": "Велика (35см)", "price_modifier": 80}]'::jsonb,
             2, true),
            ('quattro-formaggi', 'pizza', 'Чотири сири', 'Піца з чотирма видами сиру', 170.0,
             '[{"type": "Розмір", "name": "Мала (25см)", "price_modifier": 0},
               {"type": "Розмір", "name": "Середня (30см)", "price_modifier": 40},
               {"type": "Розмір", "name": "Велика (35см)", "price_modifier": 80}]'::jsonb,
             3, true),
            ('cola', 'drinks', 'Coca-Cola', 'Класична кока-кола', 30.0,
             '[{"type": "Об''єм", "name": "0.33л", "price_modifier": 0},
               {"type": "Об''єм", "name": "0.5л", "price_modifier": 10}]'::jsonb,
             1, true),
            ('water', 'drinks', 'Вода мінеральна', 'Мінеральна вода', 20.0,
             '[{"type": "Об''єм", "name": "0.5л", "price_modifier": 0},
               {"type": "Об''єм", "name": "1л", "price_modifier": 10}]'::jsonb,
             2, true)
        """))
        print("✅ Added products")
        
        # Add locations
        await session.execute(text("""
            INSERT INTO locations (location_id, city, name, address, is_active) VALUES
            ('kyiv-center', 'Київ', 'Центральний вокзал', 'вул. Вокзальна, 1', true),
            ('lviv-market', 'Львів', 'Ринок Галицький', 'пл. Ринок, 10', true),
            ('odesa-beach', 'Одеса', 'Аркадія', 'Аркадія, пляж', true)
        """))
        print("✅ Added locations")
        
        await session.commit()
    
    print("\n🎉 Database seeding completed successfully!")
    print("\nYou can now:")
    print("  • View categories at http://localhost:8000/api/categories")
    print("  • View products at http://localhost:8000/api/products")
    print("  • View locations at http://localhost:8000/api/pickup-locations")


if __name__ == "__main__":
    asyncio.run(seed_database())
