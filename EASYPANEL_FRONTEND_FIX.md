# 🔧 ИСПРАВЛЕНИЕ FRONTEND В EASYPANEL

**Проблема:** Frontend не доступен ("Service is not reachable")  
**Причина:** Неправильная конфигурация сборки в EasyPanel  
**Решение:** Обновить настройки сервиса

---

## ✅ ШАГ 1: ПРОВЕРКА ФАЙЛОВ

Убедитесь что в репозитории есть файл `frontend/Dockerfile` (без постфикса `.prod`).

✅ **Готово** - файл создан и закоммичен.

---

## 🔄 ШАГ 2: ОБНОВЛЕНИЕ В EASYPANEL

### 2.1. Откройте настройки Frontend сервиса

1. Зайдите в EasyPanel: https://your-server:3000
2. Откройте проект: **pizzamat**
3. Найдите сервис: **frontend**
4. Нажмите на него для редактирования

### 2.2. Проверьте Build настройки

В разделе **Build Configuration**:

```
Build Method: Dockerfile
Dockerfile Path: frontend/Dockerfile
Build Context: frontend
```

⚠️ **ВАЖНО:** Убедитесь что путь **НЕ** `frontend/Dockerfile.prod`

### 2.3. Добавьте Build Arguments

В разделе **Build Arguments** добавьте:

```
VITE_API_URL = https://api.pizzamat.aibusiness.kz
NODE_ENV = production
```

**Как добавить:**
1. Нажмите **"+ Add Build Arg"**
2. Name: `VITE_API_URL`
3. Value: `https://api.pizzamat.aibusiness.kz`
4. Нажмите **"+ Add Build Arg"** снова
5. Name: `NODE_ENV`
6. Value: `production`

### 2.4. Проверьте Port

В разделе **Ports**:

```
Container Port: 80
Domain: pizzamat.aibusiness.kz
Enable SSL: ✅ Yes
```

### 2.5. Проверьте Health Check (опционально)

Если есть раздел **Health Check**, настройте:

```
Type: HTTP
Port: 80
Path: /health
Interval: 30s
Timeout: 10s
Retries: 3
```

### 2.6. Сохраните изменения

Нажмите **"Save"** или **"Update"** (зависит от версии EasyPanel)

---

## 🚀 ШАГ 3: ПЕРЕСБОРКА

### 3.1. Pull последних изменений

EasyPanel должен автоматически подтянуть изменения из GitHub.

Если не подтянул:
1. В сервисе **frontend** нажмите **"Pull Latest"** или **"Sync"**
2. Подтвердите действие

### 3.2. Rebuild контейнера

**⚠️ ОБЯЗАТЕЛЬНО: Полная пересборка!**

1. В сервисе **frontend** нажмите **"Rebuild"** или **"Redeploy"**
2. Выберите опцию **"Force rebuild"** или **"No cache"** если доступна
3. Нажмите **"Confirm"**

### 3.3. Следите за процессом сборки

1. Перейдите на вкладку **"Logs"** или **"Build Logs"**
2. Следите за прогрессом сборки
3. Ожидайте 3-5 минут

**Что должно быть в логах:**

```
Step 1/X : FROM node:20-alpine AS builder
Step 2/X : WORKDIR /app
...
Step X/X : CMD ["nginx", "-g", "daemon off;"]
Successfully built [image-id]
Successfully tagged [image-name]
```

### 3.4. Проверьте статус

После завершения сборки:

1. Статус контейнера должен стать **"Running"** (зеленый)
2. Health check (если настроен) должен показывать **"Healthy"**

---

## ✅ ШАГ 4: ПРОВЕРКА

### 4.1. Проверьте логи контейнера

1. Вкладка **"Logs"** (Runtime Logs, не Build Logs)
2. Вы должны увидеть:

```
nginx: [notice] start worker processes
nginx: [notice] start worker process 1
```

**Теперь логи должны появляться!** При открытии сайта увидите:

```
10.x.x.x - - [date] "GET / HTTP/1.1" 200 xxxx "-" "Mozilla/5.0..."
```

### 4.2. Проверьте Health Check

Если настроен, попробуйте вручную:

```bash
curl http://pizzamat.aibusiness.kz/health
# Ответ: healthy
```

Или в браузере:
```
https://pizzamat.aibusiness.kz/health
```

### 4.3. Откройте сайт

```
https://pizzamat.aibusiness.kz
```

**Должна открыться главная страница приложения!**

---

## 🔍 ШАГ 5: ПРОВЕРКА API ПОДКЛЮЧЕНИЯ

### 5.1. Откройте DevTools

1. Откройте https://pizzamat.aibusiness.kz
2. Нажмите F12 (DevTools)
3. Перейдите на вкладку **"Console"**

### 5.2. Проверьте запросы

На вкладке **"Network"** должны быть запросы к:
```
https://api.pizzamat.aibusiness.kz/...
```

Если запросы идут не туда (например, к `localhost`):
- Значит VITE_API_URL не был применен при сборке
- Нужно пересобрать с правильными Build Args

### 5.3. Проверьте CORS

Если видите ошибку CORS:

```
Access to fetch at 'https://api.pizzamat.aibusiness.kz/...' from origin 'https://pizzamat.aibusiness.kz' has been blocked by CORS policy
```

**Решение:**

1. Откройте backend сервис в EasyPanel
2. Проверьте Environment Variable `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=["https://pizzamat.aibusiness.kz"]
   ```
3. Если неправильно, исправьте и перезапустите backend

---

## 🐛 TROUBLESHOOTING

### Проблема: Build fails (сборка падает)

**Симптом:**
```
ERROR: failed to solve: failed to compute cache key
```

**Решение:**
1. Убедитесь что все файлы закоммичены в Git:
   ```bash
   git add frontend/Dockerfile
   git commit -m "Add frontend Dockerfile"
   git push origin main
   ```
2. В EasyPanel: Pull Latest → Rebuild

---

### Проблема: Контейнер запускается, но сразу падает

**Проверьте логи:**
```
frontend → Logs
```

**Возможные причины:**

1. **Nginx конфигурация неправильная**
   - Проверьте синтаксис в Dockerfile
   - Пересоберите с `--no-cache`

2. **Порт уже занят**
   - Проверьте Port Mapping
   - Используется ли порт 80 другим сервисом

3. **Файлы не скопировались**
   ```bash
   # В EasyPanel Console:
   docker exec -it [container-name] sh
   ls -la /usr/share/nginx/html/
   # Должны быть: index.html, assets/, и т.д.
   ```

---

### Проблема: Сайт открывается, но пустой экран

**Проверьте DevTools Console:**

1. Откройте F12
2. Вкладка Console
3. Ищите ошибки JavaScript

**Возможные причины:**

1. **Vite build failed**
   - Проверьте Build Logs в EasyPanel
   - Должно быть: `✓ built in X seconds`

2. **Пути к файлам неправильные**
   - Откройте View Source (Ctrl+U)
   - Проверьте пути к JS/CSS файлам
   - Должны быть относительные: `/assets/...`

3. **API недоступен**
   - Проверьте Network вкладку
   - Все запросы к API должны быть успешные (200)

---

### Проблема: "Service is not reachable" все еще

**Чек-лист:**

- [ ] Dockerfile находится по пути `frontend/Dockerfile`
- [ ] Build Args добавлены: VITE_API_URL и NODE_ENV
- [ ] Build Context = `frontend`
- [ ] Dockerfile Path = `frontend/Dockerfile`
- [ ] Container Port = 80
- [ ] Domain правильно настроен
- [ ] SSL включен
- [ ] Сервис пересобран с --no-cache
- [ ] Статус контейнера = Running
- [ ] Логи показывают nginx запустился

**Если все галочки стоят:**

1. Проверьте реверс-прокси (если используется)
2. Проверьте DNS записи домена
3. Проверьте Firewall на сервере
4. Попробуйте доступ напрямую по IP:
   ```
   http://YOUR_SERVER_IP:PORT
   ```

---

## 📋 КОНТРОЛЬНЫЙ СПИСОК ДЛЯ EASYPANEL

### Frontend Service Configuration

**General:**
- [x] Service Name: `frontend`
- [x] Repository: `AiBusiness-KZ/PizzaMat`
- [x] Branch: `main` или `production`

**Build:**
- [x] Build Method: `Dockerfile`
- [x] Dockerfile Path: `frontend/Dockerfile`
- [x] Build Context: `frontend`
- [x] Build Args:
  - [x] `VITE_API_URL=https://api.pizzamat.aibusiness.kz`
  - [x] `NODE_ENV=production`

**Ports:**
- [x] Container Port: `80`
- [x] Domain: `pizzamat.aibusiness.kz`
- [x] SSL: Enabled

**Deploy:**
- [x] Restart Policy: `always`
- [x] Deploy on Push: Enabled (optional)

**Health Check (optional):**
- [ ] Type: `HTTP`
- [ ] Port: `80`
- [ ] Path: `/health`
- [ ] Interval: `30s`

---

## 🎯 ОЖИДАЕМЫЙ РЕЗУЛЬТАТ

После выполнения всех шагов:

✅ **Backend:**
```bash
curl https://api.pizzamat.aibusiness.kz/health
# {"status":"ok","version":"1.0.0","service":"pizzamatif-backend"}

curl https://api.pizzamat.aibusiness.kz/debug-info
# {"DEBUG":false,"docs_enabled":false,...}
```

✅ **Frontend:**
```bash
curl https://pizzamat.aibusiness.kz/health
# healthy

curl -I https://pizzamat.aibusiness.kz
# HTTP/2 200
# content-type: text/html
```

✅ **В браузере:**
- https://pizzamat.aibusiness.kz - открывается главная страница
- Логи в EasyPanel показывают запросы
- DevTools не показывает ошибок
- API запросы идут на правильный домен

---

## 📞 ЧТО ДАЛЬШЕ?

После успешного запуска:

1. **Проверьте функционал:**
   - Регистрация/вход
   - Просмотр меню
   - Добавление в корзину
   - Оформление заказа

2. **Настройте контент:**
   - Войдите в админку: https://pizzamat.aibusiness.kz/admin
   - Добавьте категории
   - Добавьте продукты
   - Загрузите изображения

3. **Мониторинг:**
   - Регулярно проверяйте логи
   - Настройте алерты
   - Следите за ресурсами

4. **Backup:**
   - Настройте автоматический backup в EasyPanel
   - Проверьте восстановление

---

## ✨ УСПЕХ!

Теперь ваш frontend должен работать!

**Изменения которые мы сделали:**
1. ✅ Создали `frontend/Dockerfile` для EasyPanel
2. ✅ Настроили логирование nginx
3. ✅ Добавили health check endpoint
4. ✅ Настроили SPA роутинг
5. ✅ Добавили кеширование статики
6. ✅ Настроили безопасность (headers)

**Следующие задачи:**
- Настроить Telegram Bot
- Интегрировать n8n
- Добавить платежную систему
- Запустить в продакшн!

---

**Версия:** 1.0  
**Дата:** 2025-10-29  
**Время выполнения:** 15-30 минут
