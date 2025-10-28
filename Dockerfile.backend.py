# Dockerfile для Backend (разместить в КОРНЕ репозитория)
# Файл: PizzaMat/Dockerfile.backend

FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Копируем requirements из backend
COPY backend/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код backend
COPY backend/ .

# Порт
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]