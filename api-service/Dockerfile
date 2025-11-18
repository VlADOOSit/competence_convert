# api-service/Dockerfile
FROM node:20-alpine

# Робоча директорія всередині контейнера
WORKDIR /usr/src/app

# Спочатку копіюємо тільки package*.json для кешу встановлення залежностей
COPY package*.json ./

# Встановлюємо залежності (спочатку пробуємо npm ci, якщо є package-lock)
RUN npm ci --omit=dev || npm install --omit=dev

# Тепер копіюємо решту коду сервісу
COPY . .

# Змінні середовища
ENV NODE_ENV=production
ENV PORT=3001

EXPOSE 3001

# Точка входу (у тебе сервер саме server.js в корені api-service)
CMD ["node", "server.js"]
