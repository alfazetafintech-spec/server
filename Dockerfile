# ---- Base image ----
FROM node:20-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Install system dependencies (for pdf-parse, tesseract, etc.) ----
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy package files first (better caching) ----
COPY package*.json ./

# ---- Install deps ----
RUN npm install --omit=dev

# ---- Copy app code ----
COPY . .

# ---- Expose port (Render / local) ----
EXPOSE 3000

# ---- Start server ----
CMD ["node", "index.js"]
