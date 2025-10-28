# PizzaMatIF - Автоматизация заказов пиццы через Telegram

MVP Telegram-бота для автоматизации процесса приема и обработки заказов пиццы с интеграцией AI-проверки чеков.

## 🎯 Основные возможности

- 🤖 **Telegram Bot** - регистрация, заказы, история
- 🌐 **React WebApp** - красивый каталог товаров и корзина
- 🔐 **JWT аутентификация** - безопасность
- 🎨 **Мультиязычность** - украинский, английский, русский
- 📸 **AI-проверка чеков** - GPT-4o Vision через n8n
- 📊 **Админ-панель** - управление меню, заказами, статистикой
- 🏪 **Мультиточки** - разное меню для разных городов

## 🏗️ Архитектура

```
Frontend (React 19)
    ↓
Backend (FastAPI)
    ↓
PostgreSQL + Redis
    ↓
n8n (AI workflows)
    ↓
Telegram Bot (Aiogram 3.x)
```

## 📋 Требования

- Docker & Docker Compose
- Node.js 20+ (для локальной разработки frontend)
- Python 3.11+ (для локальной разработки backend)

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd pizzamat
```

### 2. Настроить переменные окружения

```bash
cp .env.example .env
# Отредактируйте .env файл, добавьте ваши токены
```

### 3. Запустить с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f backend
```

### 4. Доступ к сервисам

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📁 Структура проекта

```
pizzamat/
├── backend/              # FastAPI приложение
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Конфигурация, безопасность
│   │   ├── models/      # SQLAlchemy модели
│   │   ├── schemas/     # Pydantic схемы
│   │   └── services/    # Бизнес-логика
│   ├── alembic/         # Миграции БД
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/            # React + Vite
│   ├── src/
│   │   ├── components/  # React компоненты
│   │   ├── pages/       # Страницы
│   │   ├── hooks/       # Кастомные хуки
│   │   ├── api/         # API клиент
│   │   └── types/       # TypeScript типы
│   ├── package.json
│   └── vite.config.ts
│
├── bot/                 # Telegram Bot (создадите вы)
│   ├── handlers/
│   ├── keyboards/
│   ├── middlewares/
│   └── main.py
│
├── n8n/                 # Workflows (создадите вы)
│   └── workflows/
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🛠️ Разработка

### Backend

```bash
# Установка зависимостей
cd backend
pip install -r requirements.txt

# Создание миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Запуск dev сервера
uvicorn app.main:app --reload
```

### Frontend

```bash
# Установка зависимостей
cd frontend
npm install

# Запуск dev сервера
npm run dev

# Сборка для production
npm run build
```

### База данных

```bash
# Подключение к PostgreSQL
docker-compose exec postgres psql -U pizzamat -d pizzamatif

# Бэкап БД
docker-compose exec postgres pg_dump -U pizzamat pizzamatif > backup.sql

# Восстановление БД
docker-compose exec -T postgres psql -U pizzamat pizzamatif < backup.sql
```

## 📝 API Документация

После запуска backend, документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные endpoints:

#### Аутентификация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `POST /api/v1/auth/validate-webapp` - Валидация Telegram WebApp

#### Меню
- `GET /api/v1/menu/cities` - Список городов
- `GET /api/v1/menu/locations?city_id={id}` - Точки выдачи
- `GET /api/v1/menu/categories?location_id={id}` - Категории
- `GET /api/v1/menu/products?location_id={id}` - Товары

#### Заказы
- `POST /api/v1/orders/calculate` - Расчет стоимости
- `POST /api/v1/orders/create` - Создание заказа
- `POST /api/v1/orders/{id}/upload-receipt` - Загрузка чека
- `GET /api/v1/orders/my-orders` - История заказов

## 🤖 Telegram Bot (инструкция для реализации)

### Создание бота

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env` файл

### Основные команды

- `/start` - Регистрация/Главное меню
- `/menu` - Открыть WebApp с меню
- `/history` - История заказов
- `/help` - Помощь

### Структура бота (рекомендуемая)

```python
# bot/main.py
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import user, admin

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    await dp.start_polling(bot)
```

Подробная документация по созданию бота будет создана после завершения Backend.

## 🔄 n8n Workflows (инструкция для реализации)

### Установка n8n

```bash
# Добавьте в docker-compose.yml:
n8n:
  image: n8nio/n8n:latest
  ports:
    - "5678:5678"
  environment:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=admin
    - N8N_BASIC_AUTH_PASSWORD=your_password
  volumes:
    - n8n_data:/home/node/.n8n
```

### Основные Workflows

1. **Receipt Validation** - Проверка чеков через GPT-4o
2. **Manager Notification** - Уведомления в менеджерский канал
3. **Order Status Updates** - Обновление статусов заказов

Подробная документация по созданию workflows будет создана после завершения Backend.

## 🌍 Мультиязычность

Проект поддерживает три языка:
- 🇺🇦 Украинский (основной)
- 🇬🇧 Английский
- 🇷🇺 Русский

Переводы находятся в:
- Backend: `backend/app/core/i18n/`
- Frontend: `frontend/src/i18n/`
- Bot: `bot/locales/`

## 🧪 Тестирование

```bash
# Backend тесты
cd backend
pytest

# Frontend тесты
cd frontend
npm run test

# E2E тесты
npm run test:e2e
```

## 📦 Деплой на production

### Подготовка

1. Обновите переменные окружения в `.env`
2. Смените все пароли и секреты
3. Настройте SSL сертификаты
4. Настройте домен

### Деплой

```bash
# Сборка production образов
docker-compose -f docker-compose.prod.yml build

# Запуск
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Полезные команды

```bash
# Остановка всех сервисов
docker-compose down

# Пересборка контейнеров
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Очистка всех данных (ОСТОРОЖНО!)
docker-compose down -v

# Вход в контейнер
docker-compose exec backend sh
docker-compose exec frontend sh

# Выполнение команд в контейнере
docker-compose exec backend alembic upgrade head
docker-compose exec postgres psql -U pizzamat
```

## 📊 Мониторинг

### Метрики

- CPU/Memory usage: `docker stats`
- Логи: `docker-compose logs -f [service]`
- Database queries: PostgreSQL logs

### Health checks

```bash
# Backend
curl http://localhost:8000/health

# Database
docker-compose exec postgres pg_isready
```

## 🐛 Troubleshooting

### База данных не запускается

```bash
# Проверить логи
docker-compose logs postgres

# Пересоздать volume
docker-compose down -v
docker-compose up -d
```

### Backend не подключается к БД

```bash
# Проверить что PostgreSQL запущен
docker-compose ps postgres

# Проверить credentials в .env
```

### Frontend не видит Backend

```bash
# Проверить VITE_API_URL в frontend/.env
# Проверить CORS настройки в backend
```

## 📚 Дополнительные ресурсы

- [FastAPI документация](https://fastapi.tiangolo.com/)
- [React документация](https://react.dev/)
- [Aiogram документация](https://docs.aiogram.dev/)
- [n8n документация](https://docs.n8n.io/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)

## 🤝 Участие в разработке

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License

## 👥 Авторы

- Backend + Frontend - AI Assistant
- Bot + n8n - Вы (по инструкции)

## 📞 Контакты

Для вопросов и предложений создавайте Issues в репозитории.

---

**Версия:** 1.0.0  
**Дата:** Октябрь 2024  
**Статус:** 🚧 В разработке
