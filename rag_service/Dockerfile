# RAG Service Dockerfile
FROM ghcr.io/prefix-dev/pixi:latest

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pixi project files and the packages it needs to install in editable mode
COPY pyproject.toml pixi.lock ./
COPY backend ./backend
COPY config ./config

# Install the locked environment (this also installs agent_swarn in editable mode)
RUN pixi install --locked

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["pixi", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
