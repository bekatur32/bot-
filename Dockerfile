# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install --no-use-pep517 -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт для вебхука
EXPOSE 8000

# Запускаем Django через gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
