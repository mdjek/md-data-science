# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /workspace

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .