# 🔐 Руководство по безопасности PizzaMat

## ⚠️ КРИТИЧНО: Перед деплоем в production

### 1. Аутентификация администратора

**Текущий статус:** ✅ Реализована JWT аутентификация

- **Дефолтные учётные данные:**
  - Username: `admin`
  - Password: `admin123`

**❗ ОБЯЗАТЕЛЬНО ИЗМЕНИТЬ перед production!**

В файле `backend/app/routes/auth.py` находится:
```python
ADMIN_CREDENTIALS = {
    "admin": {
        "password_hash": get_password_hash("admin123"),  # CHANGE THIS!
        "is_admin": True
    }
}
```

**Как изменить:**
1. Сгенерируйте надёжный пароль (мин. 16 символов)
2. Замените `"admin123"` на новый пароль
3. Рассмотрите перенос учётных данных в базу данных

### 2. Секретные ключи

**❗ НИКОГДА не используйте дефолтные значения в production!**

Сгенерируйте надёжные секреты:

```bash
# JWT Secret (минимум 64 символа)
openssl rand -hex 32

# Database Password (минимум 32 символа)
openssl rand -base64 32

# Redis Password
openssl rand -base64 24
```

### 3. Переменные окружения

**Файлы конфигурации:**
- `.env.example` - для development (можно коммитить)
- `.env.production.example` - шаблон для production
- `.env` - **НИКОГДА НЕ КОММИТИТЬ!**

**Checklist перед деплоем:**
- [ ] `JWT_SECRET` изменён на уникальный
- [ ] `POSTGRES_PASSWORD` изменён
- [ ] `REDIS_PASSWORD` установлен
- [ ] `DEBUG=false` в production
- [ ] `ALLOWED_ORIGINS` содержит только ваш домен
- [ ] Все `CHANGE_ME` значения заменены

### 4. Защищённые endpoints

**Админ панель защищена JWT:**
- `/api/admin/*` - требует валидный admin токен
- `/api/auth/login` - rate limited (5 попыток в минуту)

**Как получить токен:**
```bash
# Login request
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Response
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "is_admin": true
}

# Use token in requests
curl -X GET http://localhost:8000/api/admin/categories \
  -H "Authorization: Bearer eyJ..."
```

### 5. Rate Limiting

**Текущие лимиты:**
- Login endpoint: **5 попыток / 60 секунд**
- Admin endpoints: защищены JWT (неограниченно для авторизованных)
- Public endpoints: не ограничены

**Рекомендации для production:**
- Используйте Redis для распределённого rate limiting
- Добавьте rate limiting на public endpoints
- Настройте WAF/CDN (Cloudflare)

### 6. Валидация файлов

**Реализованная защита:**
- ✅ Проверка расширения файла
- ✅ Проверка MIME-type
- ✅ Проверка magic bytes (реальное содержимое)
- ✅ Ограничение размера файла (10MB)
- ✅ Проверка на пустые файлы
- ✅ Sanitization имени файла

**Допустимые форматы изображений:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)

### 7. Database Security

**Best practices:**
1. Используйте сильные пароли (мин. 32 символа)
2. Ограничьте сетевой доступ (только localhost или VPN)
3. Регулярные бэкапы
4. Логирование запросов
5. SSL/TLS соединения в production

**В docker-compose.prod.yml:**
```yaml
postgres:
  ports:
    - "127.0.0.1:5432:5432"  # Только localhost!
```

### 8. CORS Configuration

**Development:**
```python
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

**Production:**
```python
ALLOWED_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

**Не используйте:**
- `allow_origins=["*"]` - разрешает любой домен
- HTTP в production (только HTTPS!)

### 9. SSL/TLS

**Обязательно в production:**
- HTTPS для frontend
- HTTPS для backend API
- HTTPS для webhooks

**Рекомендации:**
- Let's Encrypt для бесплатных сертификатов
- Минимум TLS 1.2
- Используйте HSTS заголовки

### 10. Логирование и мониторинг

**Что логировать:**
- ✅ Неудачные попытки входа
- ✅ Изменения в admin панели
- ✅ Upload файлов
- ✅ Ошибки приложения
- ⚠️ НЕ логировать пароли и токены!

**Рекомендуемые инструменты:**
- Sentry для error tracking
- ELK/Grafana для метрик
- CloudWatch/Datadog в облаке

---

## 🛡️ Checklist безопасности

### Перед первым запуском:
- [ ] Изменён admin пароль
- [ ] Сгенерированы уникальные секреты
- [ ] Создан `.env` файл из `.env.production.example`
- [ ] `.env` добавлен в `.gitignore` (уже сделано)

### Перед деплоем:
- [ ] `DEBUG=false`
- [ ] HTTPS настроен
- [ ] CORS ограничен вашим доменом
- [ ] Database password сильный (мин. 32 символа)
- [ ] JWT secret уникальный (мин. 64 символа)
- [ ] Redis password установлен
- [ ] Rate limiting настроен
- [ ] Логирование работает
- [ ] Backups настроены

### После деплоя:
- [ ] Тест авторизации
- [ ] Тест rate limiting
- [ ] Тест file upload validation
- [ ] Проверка логов
- [ ] Scan на уязвимости (например, OWASP ZAP)

---

## 🚨 Известные проблемы и ограничения

### 1. Hardcoded admin credentials
**Статус:** ⚠️ Временное решение для MVP

**Проблема:** Учётные данные администратора захардкожены в коде

**План исправления:**
- Создать таблицу Users в БД
- Хеширование паролей с bcrypt
- Возможность смены пароля
- Многопользовательская поддержка

### 2. In-memory rate limiting
**Статус:** ⚠️ Не подходит для production с несколькими инстансами

**Проблема:** Rate limiting хранится в памяти приложения

**План исправления:**
- Использовать Redis для distributed rate limiting
- Интеграция с slowapi или similar

### 3. No email verification
**Статус:** 📝 Не критично для текущего MVP

**План исправления:**
- Добавить email verification для новых пользователей
- Восстановление пароля по email

---

## 📞 Сообщить об уязвимости

Если вы нашли уязвимость в системе безопасности:

1. **НЕ создавайте публичный issue**
2. Отправьте описание на: security@yourdomain.com
3. Включите:
   - Описание уязвимости
   - Шаги для воспроизведения
   - Потенциальное влияние
   - Возможное решение (если есть)

Мы ответим в течение 48 часов.

---

**Последнее обновление:** Октябрь 2024  
**Версия:** 1.0.0
