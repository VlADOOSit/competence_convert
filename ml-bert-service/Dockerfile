# ml-bert-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Може знадобитися для torch/transformers
RUN apt-get update && apt-get install -y \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# Спочатку requirements.txt – щоб кешувати установку залежностей
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Потім копіюємо решту коду сервісу
COPY . .

EXPOSE 8000

# Запуск FastAPI через uvicorn (main.py, app = FastAPI())
CMD ["python", "main.py"]