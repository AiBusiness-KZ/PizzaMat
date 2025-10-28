# 📝 Changelog - PizzaMat Security & Production Updates

## [1.1.0] - 2024-10-28

### 🔐 Security Improvements

#### ✅ Реализована JWT аутентификация
- Создан модуль `backend/app/core/dependencies.py` с функциями авторизации
- Добавлен `backend/app/routes/auth.py` с endpoint'ом login
- Все admin routes защищены JWT токенами
- Дефолтные учётные данные: admin/admin123 (**ИЗМЕНИТЬ в production!**)

#### ✅ Добавлен Rate Limiting
- Создан модуль `backend/app/core/rate_limit.py`
- Login endpoint ограничен: 5 попыток / 60 секунд
- Защита от brute-force атак
- In-memory implementation (для production рекомендуется Redis)

#### ✅ Улучшена валидация файлов
- Создан модуль `backend/app/core/file_validation.py`
- Проверка реального содержимого файла (magic bytes)
- Проверка MIME-type и расширения
- Ограничение размера файла (10MB)
- Sanitization имён файлов
- Защита от path traversal атак

### 🗂️ Структурные изменения

#### ✅ Удалены лишние файлы и директории
- Удалена директория `Draft-Fronend/` (старая версия)
- Удалён `.env` файл из репозитория (**критично для безопасности!**)

#### ✅ Обновлён .gitignore
- Добавлены паттерны для `.venv/` и `**/.venv/`
- Улучшено игнорирование `.env` файлов
- Исправлено игнорирование Alembic миграций

#### ✅ Созданы .dockerignore файлы
- `backend/.dockerignore` - исключает ненужные файлы из Docker образа
- `frontend/.dockerignore` - оптимизирует размер frontend образа
- Улучшена скорость сборки Docker образов

### 🚀 Production Ready

#### ✅ Создан docker-compose.prod.yml
- Production конфигурация с улучшенной безопасностью
- Порты привязаны только к localhost
- Redis с паролем
- Backend с 4 workers
- Настроено логирование

#### ✅ Создан .env.production.example
- Шаблон для production environment variables
- Подробные комментарии для каждой переменной
- Инструкции по генерации секретов

#### ✅ Создана документация SECURITY.md
- Checklist безопасности перед деплоем
- Инструкции по настройке аутентификации
- Рекомендации по production deployment
- Известные ограничения и их решения

### 📚 Документация

#### Новые файлы:
- `SECURITY.md` - руководство по безопасности
- `CHANGELOG.md` - история изменений
- `.env.production.example` - шаблон для production
- `docker-compose.prod.yml` - production конфигурация

### 🔧 Технические улучшения

#### Backend:
- Добавлена валидация `base_price` (не может быть отрицательной)
- Улучшена обработка ошибок в file uploads
- Добавлены security middleware
- Оптимизированы imports

#### Infrastructure:
- Docker образы оптимизированы с .dockerignore
- Логирование настроено с ротацией
- Health checks улучшены
- Volumes правильно настроены

---

## Следующие шаги (TODO)

### 🔴 Критично перед production:
1. Изменить admin пароль в `backend/app/routes/auth.py`
2. Сгенерировать уникальные секреты для `.env`
3. Настроить HTTPS/SSL
4. Настроить Nginx reverse proxy
5. Настроить domain и DNS

### 🟠 Важно:
1. Перенести admin credentials в базу данных
2. Реализовать Redis-based rate limiting
3. Добавить email verification
4. Настроить automated backups
5. Добавить monitoring (Sentry, Grafana)

### 🟡 Желательно:
1. Реализовать Telegram Bot
2. Настроить n8n workflows  
3. Добавить unit tests
4. Настроить CI/CD pipeline
5. Добавить audit logging

---

## Миграция с v1.0.0

### Что нужно сделать:

1. **Обновите зависимости:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Создайте новый .env файл:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env
   ```

3. **Обновите admin пароль:**
   - Откройте `backend/app/routes/auth.py`
   - Измените дефолтный пароль

4. **Перезапустите сервисы:**
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

5. **Проверьте работу аутентификации:**
   ```bash
   # Test login
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

---

## Breaking Changes

### ⚠️ Admin API теперь требует аутентификацию

**Было:**
```bash
curl http://localhost:8000/api/admin/categories
```

**Стало:**
```bash
# 1. Получить токен
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# 2. Использовать токен
curl http://localhost:8000/api/admin/categories \
  -H "Authorization: Bearer $TOKEN"
```

### Frontend dataProvider

Frontend должен хранить JWT токен и отправлять в каждом запросе:

```typescript
// localStorage.setItem('token', response.access_token)
const token = localStorage.getItem('token');
headers: {
  'Authorization': `Bearer ${token}`
}
```

---

## Тестирование

### Проверка безопасности:

```bash
# 1. Rate limiting на login
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"wrong"}'
  echo ""
done
# Ожидается: 6-й запрос вернёт 429 Too Many Requests

# 2. Admin endpoint без токена
curl http://localhost:8000/api/admin/categories
# Ожидается: 401 Unauthorized

# 3. File upload валидация
curl -X POST http://localhost:8000/api/admin/upload/image \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@malicious.exe"
# Ожидается: 400 Bad Request
```

---

**Версия:** 1.1.0  
**Дата:** 28 октября 2024  
**Автор:** AI Assistant
