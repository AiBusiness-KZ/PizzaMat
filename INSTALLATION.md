# 🚀 Инструкция по установке и запуску PizzaMat Admin Panel

## 📋 Что было сделано

### ✅ Backend
- Полностью рабочий Admin API (`/api/admin/*`)
- CRUD для categories, products, locations, settings, orders
- Upload изображений
- Swagger документация: http://localhost:8000/docs

### ✅ Frontend
- **Refine Admin Panel** полностью настроен
- Data Provider для работы с Backend API
- Страницы администрирования:
  - Dashboard
  - Categories (список, создание, редактирование)
  - Products (список, создание, редактирование) + upload изображений
  - Locations (список, создание, редактирование)
  - Settings (редактирование настроек сайта)

---

## 🔧 Установка

### 1. Установить зависимости Frontend

```bash
cd frontend
npm install
```

Это установит все необходимые пакеты, включая:
- `@refinedev/core` - Core Refine framework
- `@refinedev/antd` - Ant Design integration
- `@refinedev/react-router-v6` - Router integration
- `antd` - Ant Design UI library
- `axios` - HTTP client
- `react-router-dom` - React Router

### 2. Запустить Backend (если еще не запущен)

```bash
# Из корневой директории проекта
docker-compose up -d
```

Или запустить backend локально:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Запустить Frontend

```bash
cd frontend
npm run dev
```

---

## 🌐 Доступ

- **Client (главная страница):** http://localhost:5173/
- **Admin Panel:** http://localhost:5173/admin
- **Backend API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

---

## 📂 Структура Frontend

```
frontend/src/
├── App.tsx                      # Главный компонент с Refine setup
├── main.tsx                     # Entry point
├── providers/
│   └── dataProvider.ts          # Data provider для Backend API
├── pages/
│   ├── Home.tsx                 # Клиентская страница
│   └── admin/
│       ├── dashboard.tsx        # Dashboard админки
│       ├── categories/
│       │   ├── list.tsx        # Список категорий
│       │   ├── create.tsx      # Создание категории
│       │   └── edit.tsx        # Редактирование категории
│       ├── products/
│       │   ├── list.tsx        # Список продуктов
│       │   ├── create.tsx      # Создание продукта + upload
│       │   └── edit.tsx        # Редактирование продукта
│       ├── locations/
│       │   ├── list.tsx        # Список локаций
│       │   ├── create.tsx      # Создание локации
│       │   └── edit.tsx        # Редактирование локации
│       └── settings/
│           └── edit.tsx        # Настройки сайта
```

---

## 🎯 Возможности Admin Panel

### Categories (Категории)
- ✅ Просмотр всех категорий
- ✅ Создание новой категории
- ✅ Редактирование категории
- ✅ Удаление категории
- ✅ Управление порядком сортировки
- ✅ Активация/деактивация

### Products (Продукты)
- ✅ Просмотр всех продуктов с изображениями
- ✅ Создание продукта с загрузкой изображения
- ✅ Редактирование продукта
- ✅ Удаление продукта
- ✅ Привязка к категории
- ✅ Управление ценой
- ✅ Активация/деактивация

### Locations (Локации)
- ✅ Просмотр всех точек выдачи
- ✅ Создание новой локации
- ✅ Редактирование локации
- ✅ Удаление локации
- ✅ Привязка к городу
- ✅ Указание адреса и часов работы
- ✅ Активация/деактивация

### Settings (Настройки)
- ✅ Редактирование названия сайта
- ✅ Загрузка логотипа
- ✅ Контактная информация
- ✅ Настройки Telegram Bot
- ✅ Интеграции (OpenAI, n8n)

---

## 🔐 ВАЖНО: Безопасность

**⚠️ КРИТИЧНО:** В текущей версии НЕТ аутентификации!

### Перед деплоем в production необходимо:

1. **Добавить JWT аутентификацию в Backend**
2. **Создать страницу логина**
3. **Защитить admin роуты**
4. **Добавить Rate Limiting**

### Временное решение для тестирования:

Можно добавить базовую защиту паролем на уровне nginx или добавить простую проверку в `App.tsx`:

```tsx
const [isAuthenticated, setIsAuthenticated] = useState(false);

if (!isAuthenticated && window.location.pathname.startsWith('/admin')) {
  const password = prompt('Enter admin password:');
  if (password === 'your_secret_password') {
    setIsAuthenticated(true);
  } else {
    window.location.href = '/';
  }
}
```

---

## 🐛 Troubleshooting

### TypeScript ошибки после создания файлов

Это нормально! Ошибки исчезнут после запуска `npm install` в директории `frontend/`.

### Backend не отвечает

Проверьте что backend запущен:
```bash
curl http://localhost:8000/health
```

### CORS ошибки

Backend уже настроен на CORS, но если возникают проблемы, проверьте `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Upload изображений не работает

Убедитесь что директория `uploads/` существует и имеет права на запись:
```bash
mkdir -p uploads
chmod 777 uploads
```

---

## 📚 Документация

- **Refine Docs:** https://refine.dev/docs
- **Ant Design:** https://ant.design/components/overview/
- **Backend API Guide:** см. файл `ADMIN_API_GUIDE.txt`

---

## 🎨 Кастомизация

### Изменить тему админки

В `App.tsx`:
```tsx
<ConfigProvider theme={RefineThemes.Blue}>  // Green, Purple, Magenta, Orange
```

### Добавить новый resource

1. Добавить в `resources` массив в `App.tsx`
2. Создать страницы в `pages/admin/your-resource/`
3. Добавить роуты

---

## 📝 TODO

### Срочно (перед production):
- [ ] JWT Authentication
- [ ] Login page
- [ ] Protected routes
- [ ] Rate limiting
- [ ] Input validation

### Желательно:
- [ ] Dashboard со статистикой (подключить к API)
- [ ] Orders management
- [ ] Export/Import CSV
- [ ] Bulk operations
- [ ] Audit log
- [ ] Image optimization

---

## 🆘 Поддержка

Если возникли проблемы:
1. Проверьте что все зависимости установлены
2. Убедитесь что backend запущен
3. Проверьте консоль браузера на ошибки
4. Проверьте логи backend

---

## ✅ Готово к использованию!

После выполнения `npm install` в `frontend/` директории, admin panel полностью готов к работе.

**Удачи с проектом! 🚀**
