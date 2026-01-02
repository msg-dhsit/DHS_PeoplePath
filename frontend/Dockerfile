FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build || true
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
