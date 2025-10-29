# Використовуємо офіційний образ Python
FROM python:3.12

# Робоча директорія всередині контейнера
WORKDIR /app

# Копіюємо файл із залежностями
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Відкриваємо порт 8000 (для Django)
EXPOSE 8000

# Запускаємо сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]