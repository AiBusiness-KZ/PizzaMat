# Инструкция по заполнению базы данных тестовыми данными

## Способ 1: Запуск из Docker контейнера (Рекомендуемый)

### Шаг 1: Убедитесь, что сервисы запущены

```bash
docker-compose ps
```

Должны быть активны: `backend`, `postgres`, `redis`

### Шаг 2: Выполните seed скрипт

```bash
docker-compose exec backend python scripts/seed_simple.py
```

### Ожидаемый результат:

```
Starting database seeding...
✅ Added categories
✅ Added products
✅ Added locations

🎉 Database seeding completed successfully!

You can now:
  • View categories at http://localhost:8000/api/categories
  • View products at http://localhost:8000/api/products
  • View locations at http://localhost:8000/api/pickup-locations
```

### Что будет добавлено:

#### Категории (3 шт):
1. **Піца** (Pizza)
2. **Напої** (Drinks)
3. **Закуски** (Snacks)

#### Продукты (5 шт):
1. **Маргарита** - класична піца з томатами та моцарелою (120 грн)
2. **Пепероні** - піца з пікантною салямі (150 грн)
3. **Чотири сири** - піца з чотирма видами сиру (170 грн)
4. **Coca-Cola** - класична кока-кола (30 грн)
5. **Вода мінеральна** - мінеральна вода (20 грн)

#### Локации (3 шт):
1. **Київ** - Центральний вокзал (вул. Вокзальна, 1)
2. **Львів** - Ринок Галицький (пл. Ринок, 10)
3. **Одеса** - Аркадія (Аркадія, пляж)

---

## Способ 2: Запуск напрямую (если Python установлен локально)

### Шаг 1: Перейдите в директорию backend

```bash
cd backend
```

### Шаг 2: Установите зависимости (если еще не установлены)

```bash
pip install -r requirements.txt
```

### Шаг 3: Запустите скрипт

```bash
python scripts/seed_simple.py
```

---

## Проверка результатов

### Через API (в браузере или Postman):

1. **Категории**: http://localhost:8000/api/categories
2. **Продукты**: http://localhost:8000/api/products
3. **Локации**: http://localhost:8000/api/pickup-locations

### Через Frontend:

Откройте http://localhost:5173 или http://pizzamat.aibusiness.kz
- Должны отображаться категории в верхней навигации
- Должны отображаться карточки товаров
- В выпадающем списке должны быть точки выдачи

### Через Admin панель:

Откройте http://localhost:5173/admin или http://pizzamat.aibusiness.kz/admin
- Проверьте списки категорий, продуктов и локаций

---

## Устранение проблем

### Ошибка: "No module named 'app'"

**Решение**: Убедитесь, что запускаете скрипт из контейнера или из директории `backend`

```bash
# Если из Docker:
docker-compose exec backend python scripts/seed_simple.py

# Если локально:
cd backend
python scripts/seed_simple.py
```

### Ошибка: "TRUNCATE ... cannot run inside a transaction block"

**Решение**: Это нормально, скрипт автоматически обрабатывает эту ситуацию. Данные все равно будут добавлены.

### Ошибка подключения к базе данных

**Решение**: Проверьте, что PostgreSQL запущен:

```bash
docker-compose ps postgres
docker-compose logs postgres
```

Перезапустите сервисы при необходимости:

```bash
docker-compose restart postgres
docker-compose restart backend
```

---

## Очистка базы данных

Если нужно очистить БД и заполнить заново:

```bash
# Скрипт автоматически очищает таблицы перед добавлением данных
docker-compose exec backend python scripts/seed_simple.py
```

Или вручную через psql:

```bash
docker-compose exec postgres psql -U pizzamat -d pizzamatif

# В psql:
TRUNCATE categories, products, locations RESTART IDENTITY CASCADE;
\q
```

Затем запустите seed скрипт снова.

---

## Добавление своих данных

Если нужно добавить свои данные, отредактируйте файл `backend/scripts/seed_simple.py`:

1. Найдите секции INSERT INTO
2. Добавьте свои данные по аналогии с существующими
3. Запустите скрипт

**Важно**: Соблюдайте формат JSON для поля `options` в продуктах.
