"""
Production seed script - adapted to current DB structure
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import async_session_maker


async def seed_database():
    """Seed database with test data"""
    print("🌱 Starting database seeding...")
    
    async with async_session_maker() as session:
        # Clear existing data (be careful in production!)
        print("⚠️  Clearing existing data...")
        await session.execute(text("TRUNCATE cities, categories, products, locations RESTART IDENTITY CASCADE"))
        
        # Add cities
        print("📍 Adding cities...")
        await session.execute(text("""
            INSERT INTO cities (name, is_active) VALUES
            ('Київ', true),
            ('Львів', true),
            ('Одеса', true),
            ('Алмати', true)
        """))
        print("✅ Added 4 cities")
        
        # Add categories
        print("📂 Adding categories...")
        await session.execute(text("""
            INSERT INTO categories (name, description, sort_order, is_active) VALUES
            ('Піца', 'Смачні піци з різними начинками', 1, true),
            ('Напої', 'Холодні та гарячі напої', 2, true),
            ('Закуски', 'Смачні закуски та снеки', 3, true),
            ('Десерти', 'Солодкі десерти', 4, true)
        """))
        print("✅ Added 4 categories")
        
        # Add products
        print("🍕 Adding products...")
        await session.execute(text("""
            INSERT INTO products (category_id, name, description, base_price, sort_order, is_active) VALUES
            -- Піца
            (1, 'Маргарита', 'Класична піца з томатами та моцарелою', 120.00, 1, true),
            (1, 'Пепероні', 'Піца з пікантною салямі пепероні', 150.00, 2, true),
            (1, 'Чотири сири', 'Піца з чотирма видами сиру', 170.00, 3, true),
            (1, 'Гавайська', 'Піца з куркою та ананасами', 160.00, 4, true),
            (1, 'М''ясна', 'Піца з трьома видами м''яса', 180.00, 5, true),
            -- Напої
            (2, 'Coca-Cola 0.33л', 'Класична кока-кола', 30.00, 1, true),
            (2, 'Coca-Cola 0.5л', 'Класична кока-кола', 40.00, 2, true),
            (2, 'Fanta 0.33л', 'Апельсиновий напій', 30.00, 3, true),
            (2, 'Sprite 0.33л', 'Лимонний напій', 30.00, 4, true),
            (2, 'Вода мінеральна 0.5л', 'Мінеральна вода', 20.00, 5, true),
            (2, 'Сік яблучний 0.33л', 'Натуральний яблучний сік', 35.00, 6, true),
            -- Закуски
            (3, 'Картопля фрі', 'Смажена картопля з соусом', 60.00, 1, true),
            (3, 'Нагетси курячі', '6 шт курячих нагетсів', 70.00, 2, true),
            (3, 'Сирні палички', '8 шт сирних паличок', 80.00, 3, true),
            -- Десерти
            (4, 'Чізкейк', 'Класичний чізкейк', 90.00, 1, true),
            (4, 'Тірамісу', 'Італійський десерт', 95.00, 2, true)
        """))
        print("✅ Added 16 products")
        
        # Add locations
        print("📍 Adding locations...")
        await session.execute(text("""
            INSERT INTO locations (city_id, name, address, working_hours, is_active) VALUES
            (1, 'Центральний вокзал', 'вул. Вокзальна, 1', '08:00-22:00', true),
            (1, 'ТЦ Мега', 'пр. Перемоги, 5', '10:00-22:00', true),
            (2, 'Ринок Галицький', 'пл. Ринок, 10', '09:00-21:00', true),
            (2, 'ТЦ Форум', 'вул. Під Дубом, 7б', '10:00-22:00', true),
            (3, 'Аркадія', 'Аркадія, пляж', '10:00-23:00', true),
            (4, 'Мега Алматы', 'пр. Розыбакиева, 247', '10:00-22:00', true)
        """))
        print("✅ Added 6 locations")
        
        await session.commit()
    
    print("\n🎉 Database seeding completed successfully!")
    print("\n📊 Summary:")
    print("  • 4 cities")
    print("  • 4 categories")
    print("  • 16 products")
    print("  • 6 locations")
    print("\n🌐 You can now:")
    print("  • View API docs: https://api.pizzamat.aibusiness.kz/docs")
    print("  • View categories: https://api.pizzamat.aibusiness.kz/api/categories")
    print("  • View products: https://api.pizzamat.aibusiness.kz/api/products")
    print("  • Open WebApp in Telegram bot")


if __name__ == "__main__":
    asyncio.run(seed_database())