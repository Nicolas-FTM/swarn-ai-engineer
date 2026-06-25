# Build the frontend application with a Node version (mandatory to be LTS even version)
FROM node:22-alpine 

# Set working directory
WORKDIR /app/frontend

# First, copy the manifests (better cache)
COPY frontend/package.json frontend/package-lock.json ./

# Install the dependencies
RUN npm ci

# Copy the rest of the project
COPY frontend/ ./

# Expose the Vite required port
EXPOSE 5173