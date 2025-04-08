# Используем Python 3.8 как базовый образ
FROM python:3.8-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для Flask API
EXPOSE 3298

# Запускаем приложение
CMD ["python", "api_gateway/api_gateway.py"]
