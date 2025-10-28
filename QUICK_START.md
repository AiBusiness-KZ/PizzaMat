# 🚀 БЫСТРЫЙ СТАРТ - PizzaMat Admin Panel

## ⚠️ ВАЖНО: Исправлена проблема с React 19

Версии React понижены с 19 до 18 для совместимости с Refine.

---

## 📦 Установка (один раз)

### Windows:
```
.\install-admin.bat
```

Скрипт автоматически:
- Удалит старые зависимости
- Установит правильные версии пакетов
- Использует --legacy-peer-deps при необходимости

### Linux/Mac:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

## 🎯 Запуск

### Windows:
```
.\start-admin.bat
```

### Linux/Mac:
```bash
cd frontend
npm run dev
```

---

## 🌐 Доступ

После запуска откройте в браузере:

- **Client:** http://localhost:5173/
- **Admin Panel:** http://localhost:5173/admin

---

## ✅ Что работает:

### Categories (Категории)
- Список, создание, редактирование, удаление
- Управление порядком и активацией

### Products (Продукты)  
- Список, создание, редактирование, удаление
- Upload изображений
- Цены и привязка к категориям

### Locations (Локации)
- Список, создание, редактирование, удаление
- Города, адреса, часы работы

### Settings (Настройки)
- Название сайта, логотип
- Контакты
- Telegram Bot настройки
- Интеграции (OpenAI, n8n)

---

## ⚠️ ВАЖНО

**Нет аутентификации!** Не используйте в production без добавления защиты.

---

## 🛠️ Troubleshooting

### Ошибка ERESOLVE при установке
Решение: Используйте скрипт `install-admin.bat` - он автоматически использует `--legacy-peer-deps`

### npm не найден
Установите Node.js: https://nodejs.org/

### Backend не работает
```bash
# Запустите backend
docker-compose up -d
# Или
cd backend
uvicorn app.main:app --reload
```

### Порт 5173 занят
Vite автоматически выберет другой порт (5174, 5175, и т.д.)

---

Полная документация: см. `INSTALLATION.md`
