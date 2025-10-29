# n8n Workflows для PizzaMat

Этот каталог содержит примеры n8n workflows для интеграции с Telegram ботом.

## 📋 Список Workflows

### 1. Receipt Validation (AI проверка чеков)
**Файл**: `receipt_validation.json`

**Триггер**: Webhook `POST /webhook/validate-receipt`

**Что делает**:
1. Получает данные о заказе и URL изображения чека
2. Скачивает изображение
3. Отправляет в OpenAI GPT-4o Vision API
4. Анализирует чек:
   - Проверяет сумму
   - Проверяет дату
   - Проверяет читаемость
   - Определяет магазин
5. Отправляет результат обратно в Backend
6. Уведомляет менеджера в Telegram канал

**Входные данные**:
```json
{
  "order_id": 123,
  "receipt_image_url": "https://example.com/uploads/receipt_123.jpg",
  "expected_amount": 500,
  "order_code": "ABC123"
}
```

**Выходные данные** (POST к Backend `/api/orders/{order_id}/validate-result`):
```json
{
  "valid": true,
  "amount_detected": 500,
  "amount_matches": true,
  "date_valid": true,
  "readable": true,
  "confidence": 0.95,
  "notes": "Чек от магазина XYZ, сумма совпадает"
}
```

---

### 2. Manager Notifications (Уведомления менеджеру)
**Файл**: `manager_notifications.json`

**Триггер**: Webhook `POST /webhook/notify-manager`

**Что делает**:
1. Получает данные о новом заказе
2. Форматирует красивое сообщение
3. Добавляет inline клавиатуру (Подтвердить/Отклонить)
4. Отправляет в Telegram канал менеджеров

**Входные данные**:
```json
{
  "order_id": 123,
  "order_code": "ABC123",
  "user_name": "Иван Иванов",
  "user_phone": "+380501234567",
  "total_amount": 500,
  "location_name": "Улица Примерная, 10",
  "items": [
    {"name": "Маргарита", "quantity": 2, "price": 250}
  ],
  "receipt_validated": true
}
```

---

### 3. Daily Statistics (Ежедневная статистика)
**Файл**: `daily_statistics.json`

**Триггер**: Cron (ежедневно в 23:59)

**Что делает**:
1. Запрашивает статистику за день из Backend API
2. Агрегирует данные
3. Сохраняет в таблицу `bot_statistics`
4. Отправляет отчет менеджеру

---

## 🚀 Как использовать

### 1. Установите n8n

```bash
# Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Или через docker-compose (см. docker-compose.n8n.yml)
```

### 2. Импортируйте workflows

1. Откройте n8n: `http://localhost:5678`
2. Войдите/зарегистрируйтесь
3. Нажмите "Import from File"
4. Выберите файл workflow (например, `receipt_validation.json`)

### 3. Настройте credentials

#### OpenAI Credential
1. Credentials → Add Credential → OpenAI
2. API Key: ваш ключ от OpenAI
3. Save

#### HTTP Basic Auth (для защиты webhooks)
1. Credentials → Add Credential → HTTP Basic Auth
2. User: `pizzamat`
3. Password: ваш `N8N_WEBHOOK_SECRET`
4. Save

#### Telegram Bot
1. Credentials → Add Credential → Telegram Bot
2. Access Token: ваш `BOT_TOKEN`
3. Save

### 4. Активируйте workflows

1. Откройте workflow
2. Нажмите "Active" в правом верхнем углу
3. Проверьте URL webhook (если есть)

### 5. Обновите конфигурацию бота

В `.env`:
```env
N8N_URL=http://localhost:5678
N8N_WEBHOOK_SECRET=your_secret_here
```

---

## 🔧 Настройка Receipt Validation Workflow

### Prompt для GPT-4o Vision

```
Analyze this receipt image and extract the following information:

1. Total amount (number only)
2. Date (YYYY-MM-DD format)
3. Store/merchant name
4. Is the receipt readable? (yes/no)
5. Confidence level (0-1)

Expected amount: {{$json.expected_amount}} UAH
Order code: {{$json.order_code}}

Validate:
- Does the amount match the expected amount?
- Is the date within the last 24 hours?

Return ONLY valid JSON:
{
  "amount_detected": <number>,
  "date": "<YYYY-MM-DD>",
  "merchant": "<string>",
  "readable": <boolean>,
  "confidence": <0-1>,
  "amount_matches": <boolean>,
  "date_valid": <boolean>,
  "notes": "<any additional info>"
}
```

### Workflow Steps

1. **Webhook** - Receive order data
2. **HTTP Request** - Download receipt image
3. **OpenAI** - GPT-4o Vision analysis
   - Model: `gpt-4o`
   - Max Tokens: 500
   - Temperature: 0.2
   - Image: base64 encoded
4. **Function** - Parse AI response
5. **IF** - Check if valid
   - **TRUE**:
     - HTTP Request → Backend (update order status to PAID)
     - Telegram → Send to manager: "✅ Чек валідований!"
   - **FALSE**:
     - HTTP Request → Backend (set validation failed)
     - Telegram → Send to manager: "❌ Чек не пройшов перевірку"

---

## 💰 Стоимость

### OpenAI GPT-4o Vision
- ~$0.01 за изображение чека
- При 100 заказах/день = ~$1/день = ~$30/месяц

### Альтернативы:
- Google Cloud Vision API
- Azure Computer Vision
- AWS Textract
- Локальная OCR (Tesseract)

---

## 🧪 Тестирование Workflow

### 1. Тестовый запрос к webhook

```bash
curl -X POST http://localhost:5678/webhook/validate-receipt \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your_secret" \
  -d '{
    "order_id": 1,
    "receipt_image_url": "https://example.com/test_receipt.jpg",
    "expected_amount": 500,
    "order_code": "TEST123"
  }'
```

### 2. Проверка логов n8n

```bash
# Логи Docker контейнера
docker logs n8n

# Или в UI n8n:
# Executions → View execution details
```

### 3. Отладка

В n8n workflow:
1. Нажмите "Execute Workflow" (внизу справа)
2. Заполните тестовые данные
3. Проверьте каждый шаг
4. Исправьте ошибки

---

## 📊 Мониторинг

### Проверка работоспособности

```bash
# Здоровье n8n
curl http://localhost:5678/healthz

# Список активных workflows
curl http://localhost:5678/rest/workflows \
  -H "X-N8N-API-KEY: your_api_key"

# Последние executions
curl http://localhost:5678/rest/executions \
  -H "X-N8N-API-KEY: your_api_key"
```

### Метрики

- Количество успешных валидаций
- Средняя confidence
- Время обработки
- Процент false positives

Можно добавить в `bot_statistics` таблицу:
```sql
ALTER TABLE bot_statistics ADD COLUMN receipt_validation_success INTEGER DEFAULT 0;
ALTER TABLE bot_statistics ADD COLUMN receipt_validation_failed INTEGER DEFAULT 0;
ALTER TABLE bot_statistics ADD COLUMN avg_validation_confidence FLOAT DEFAULT 0;
```

---

## 🔒 Безопасность

### Защита webhooks

1. Используйте HTTPS в продакшене
2. Добавьте Basic Auth или Header validation
3. Используйте `N8N_WEBHOOK_SECRET`

### Проверка webhook секрета в workflow

Добавьте IF node в начало:
```javascript
// Expression
$execution.customData.headers['x-webhook-secret'] === 'your_secret'
```

---

## 📚 Полезные ссылки

- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 🆘 Troubleshooting

**Workflow не активируется:**
- Проверьте credentials
- Проверьте порт 5678
- Проверьте логи Docker

**OpenAI API ошибка:**
- Проверьте API ключ
- Проверьте баланс аккаунта
- Проверьте rate limits

**Telegram не получает сообщения:**
- Проверьте Bot Token
- Проверьте Channel ID (должен начинаться с -100)
- Убедитесь, что бот админ канала

---

**Создано с помощью Claude Code** 🤖
