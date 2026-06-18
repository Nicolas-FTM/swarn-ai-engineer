# Frontend Dockerfile
FROM node:21-alpine

WORKDIR /app

# Copy package files
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/vite.config.js ./
COPY frontend/index.html ./

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:5173 || exit 1

EXPOSE 5173

CMD ["npm", "run", "dev"]
