"""
Main FastAPI application entry point.
"""
# FastAPI (API REST)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# Uvicorn (Server)
import uvicorn

# Routers
from backend.app.api import (
    auxiliar,
    health
)
from backend.app.api.frontend import (
    auth,
    chat,
    users
)
from backend.app.api.rag_service import (
    documents
)
 
# Opentelemetry for Prometheus, Loki and Tempo
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from shared.utils.opentelemetry_init import init_telemetry
from shared.utils.metrics import init_metrics, get_metrics_app

# Pre and Post Actions at the time of initializing the app
from contextlib import asynccontextmanager
from backend.scripts import seed_users

# Logger setup
from shared.observability.logging_config import setup_logging
import logging

# Environment Variables
from shared.config.settings import settings

# Logger
# Configure logging
service = "backend"
setup_logging(service=service, level=settings.log_level)
logger = logging.getLogger(service)

# Measure traces
trace_provider, resource = init_telemetry(service)
init_metrics(resource)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    logger.info("Application startup")

    # Creation of dummy users 
    seed_users.main()

    logger.info("Dummy users precharged")

    
    yield
    
    logger.info("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title="Backend FastAPI Application",
    description="Backend FastAPI application with observability",
    version="0.1.0",
    lifespan=lifespan,
)

# Mount /metrics BEFORE instrumenting, so it's excluded from traced/measured routes
app.mount("/metrics", get_metrics_app())
FastAPIInstrumentor().instrument_app(app)

# Middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    logger.exception("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(auxiliar.router)

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app", 
        host="0.0.0.0",
        port=8000, 
        reload=settings.environment == "development",
    )
   