# Backend Dockerfile
FROM ghcr.io/prefix-dev/pixi:latest

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# First, copy the manifests (better cache)
# Copy pixi project files and the packages it needs to install in editable mode
COPY backend/pyproject.toml backend/pixi.lock ./

# Install the locked environment (this also installs agent_swarn in editable mode)
RUN pixi install --locked

COPY backend ./backend
COPY config ./config
COPY shared ./shared

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["pixi", "run", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]