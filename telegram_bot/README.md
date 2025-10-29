# PizzaMat Telegram Bot

Telegram бот на Aiogram 3.x для автоматизации заказов пиццы с полным отслеживанием диалогов и аналитикой.

## 🚀 Возможности

### Для клиентов:
- ✅ Регистрация через бота (телефон, имя, город)
- 🍕 Просмотр меню через Telegram WebApp
- 📦 Оформление заказов
- 📸 Загрузка чека оплаты
- ✅ AI валидация чека через n8n + GPT-4o Vision
- 📋 История заказов
- 💬 Обратная связь с менеджером

### Для менеджеров:
- 📊 Полная статистика через API
- 👁️ Отслеживание всех диалогов
- 📈 Аналитика по входам, заказам, отказам
- 🔔 Уведомления о новых заказах
- ✅/❌ Подтверждение/отклонение заказов

## 📁 Структура

```
telegram_bot/
├── bot.py                   # Главный файл бота
├── config.py                # Настройки из .env
├── handlers/                # Обработчики команд и сообщений
│   ├── start.py            # Регистрация
│   ├── menu.py             # Меню и каталог
│   ├── orders.py           # Управление заказами
│   ├── support.py          # Поддержка
│   └── manager.py          # Действия менеджера
├── keyboards/               # Клавиатуры и кнопки
│   └── main_menu.py        # Все клавиатуры
├── states/                  # FSM состояния
│   └── registration.py     # Состояния для процессов
├── middlewares/             # Промежуточное ПО
│   ├── auth_middleware.py  # Проверка регистрации
│   └── logging_middleware.py  # КЛЮЧЕВОЕ! Логирование всех действий
├── services/                # Внешние сервисы
│   ├── api_client.py       # Клиент для Backend API
│   └── n8n_client.py       # Клиент для n8n webhooks
└── utils/                   # Утилиты
```

## 🔑 Ключевая особенность: Логирование диалогов

**Все взаимодействия пользователей с ботом автоматически логируются!**

### Что логируется:

1. **Сессии** (`user_sessions`)
   - Начало и конец сессии
   - Длительность
   - Количество сообщений, команд, кликов
   - Платформа пользователя

2. **Взаимодействия** (`bot_interactions`)
   - Каждая команда (`/start`, `/menu`, etc.)
   - Каждое сообщение
   - Каждый клик по кнопке (callback_query)
   - Загрузка фото
   - Текущее FSM состояние
   - Ответ бота
   - Ошибки (если были)

3. **Сообщения поддержки** (`support_messages`)
   - Все обращения в поддержку
   - Ответы менеджера
   - Время отклика
   - Связь с заказами

### Просмотр диалогов менеджером:

```bash
# API эндпоинты для менеджера:

# Общая статистика
GET /api/analytics/dashboard?days=7

# История взаимодействий конкретного пользователя
GET /api/analytics/interactions?telegram_id=123456789&days=30

# Сессии пользователя
GET /api/analytics/sessions?user_id=1&days=7

# Сообщения поддержки
GET /api/analytics/support-messages?status=open

# Полный путь пользователя (journey)
GET /api/analytics/user-journey/123456789?days=30
```

## 🛠️ Настройка

### 1. Создайте бота в Telegram

```bash
# 1. Найдите @BotFather в Telegram
# 2. Отправьте /newbot
# 3. Следуйте инструкциям
# 4. Получите токен бота
```

### 2. Создайте канал для менеджеров

```bash
# 1. Создайте приватный канал
# 2. Добавьте бота как администратора
# 3. Получите ID канала (используйте @getidsbot)
```

### 3. Настройте переменные окружения

Добавьте в `.env`:

```env
# Telegram Bot
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MANAGER_CHANNEL_ID=-1001234567890
ADMIN_TELEGRAM_IDS=123456789,987654321

# Backend
BACKEND_URL=http://backend:8000
WEBAPP_URL=http://localhost:5173

# n8n (опционально)
N8N_URL=http://localhost:5678
N8N_WEBHOOK_SECRET=your_secret_here
```

### 4. Запустите через Docker

```bash
# Запустить все сервисы (включая бота)
docker-compose up -d

# Логи бота
docker logs -f pizzamat_bot

# Остановить бота
docker-compose stop telegram_bot

# Перезапустить бота
docker-compose restart telegram_bot
```

## 📊 Архитектура отслеживания

```
Пользователь → Telegram API
    ↓
Aiogram Bot
    ↓
SessionTrackingMiddleware
    ├─ Создает UserSession при первом взаимодействии
    └─ Хранит session_id в контексте
    ↓
AuthMiddleware
    ├─ Проверяет регистрацию пользователя
    └─ Загружает данные пользователя
    ↓
InteractionLoggingMiddleware
    ├─ Логирует каждое действие в BotInteraction
    ├─ Записывает: тип, команду, текст, FSM состояние
    ├─ Фиксирует ответ бота
    └─ Сохраняет ошибки (если были)
    ↓
Handler
    ├─ Обрабатывает запрос
    └─ Возвращает ответ пользователю
    ↓
Backend API
    └─ Сохраняет в PostgreSQL
```

## 🤖 n8n Интеграция

Бот триггерит n8n workflows для:

1. **AI валидация чеков**
   ```
   POST /webhook/validate-receipt
   {
     "order_id": 123,
     "receipt_image_url": "...",
     "expected_amount": 500,
     "order_code": "ABC123"
   }
   ```

2. **Уведомления менеджерам**
   ```
   POST /webhook/notify-manager
   {
     "order_id": 123,
     "order_code": "ABC123",
     "user_name": "John Doe",
     "total_amount": 500,
     ...
   }
   ```

См. `n8n_workflows/` для примеров workflows.

## 📈 Статистика для менеджера

### Dashboard

```python
{
  "users": {
    "total": 1523,
    "new": 45,      # За период
    "active": 234   # За период
  },
  "sessions": {
    "total": 890,
    "avg_duration_seconds": 342
  },
  "orders": {
    "created": 156,
    "paid": 142,
    "completed": 138,
    "cancelled": 4,
    "conversion_rate": 88.46
  },
  "support": {
    "tickets_opened": 23,
    "tickets_closed": 19
  }
}
```

### User Journey (Путь пользователя)

Для каждого пользователя можно увидеть:
- Все сессии
- Все команды и сообщения
- Все заказы
- Все обращения в поддержку
- Временная линия действий

## 🧪 Тестирование

```bash
# Запустите бота локально
cd telegram_bot
python bot.py

# В Telegram найдите вашего бота
# Отправьте /start

# Проверьте логи
tail -f logs/bot/bot.log

# Проверьте базу данных
docker exec -it pizzamat_postgres psql -U pizzamat -d pizzamatif
SELECT * FROM bot_interactions ORDER BY created_at DESC LIMIT 10;
```

## 📝 Команды бота

- `/start` - Регистрация или приветствие
- `/menu` - Открыть меню (WebApp)
- `/orders` - История заказов
- `/support` - Связаться с поддержкой
- `/help` - Помощь

## 🔧 Разработка

### Добавление нового handler

```python
# handlers/new_feature.py
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message(Command("new"))
async def cmd_new(message: Message, user: dict):
    language = user.get("language", "uk")
    await message.answer("New feature!")

# bot.py
from handlers import new_feature
dp.include_router(new_feature.router)
```

### Добавление нового FSM

```python
# states/new_states.py
from aiogram.fsm.state import State, StatesGroup

class NewStates(StatesGroup):
    step_1 = State()
    step_2 = State()
```

## 📚 Зависимости

- `aiogram==3.15.0` - Telegram Bot Framework
- `httpx` - HTTP клиент для API
- `asyncpg` - PostgreSQL драйвер
- `sqlalchemy` - ORM (для логирования)
- `pydantic` - Валидация данных

## 🐛 Troubleshooting

**Бот не отвечает:**
- Проверьте токен: `echo $BOT_TOKEN`
- Проверьте логи: `docker logs pizzamat_bot`
- Проверьте Backend: `curl http://localhost:8000/health`

**Логирование не работает:**
- Проверьте подключение к БД
- Проверьте таблицы: `user_sessions`, `bot_interactions`
- Запустите миграции: `alembic upgrade head`

**n8n не получает webhooks:**
- Проверьте `N8N_URL` в .env
- Проверьте доступность n8n: `curl http://localhost:5678`
- Проверьте логи бота на ошибки n8n

## 📄 Лицензия

MIT

## 👨‍💻 Автор

Generated with Claude Code
