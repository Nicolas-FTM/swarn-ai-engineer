# Builder stage - Build the frontend application
FROM node:21-alpine

# Set working directory
WORKDIR /app

# First, copy the manifests (better cache)
COPY frontend/package.json frontend/package-lock.json ./

# Install the dependencies
RUN npm ci

# Copy the rest of the project
COPY frontend/ .

# Expose the Vite required port
EXPOSE 5173

# IMPORTANT: --host 0.0.0.0 so that it works within Docker
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]