"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
import logging
from backend.app.api import auxiliar
from backend.app.api.backend import chat, users
from backend.app.api.rag_service import documents
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from backend.app.api import health

from shared.utils.logging_config import JSONFormatter, setup_logging
from shared.utils.opentelemetry_init import init_telemetry
from shared.utils.metrics import init_metrics, get_metrics_app
from shared.config import settings

from backend.scripts import seed_users

# Configure logging
setup_logging(level=settings.log_level)
logger = logging.getLogger("backend")

# Measure traces
trace_provider, resource = init_telemetry("backend")
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
app.include_router(health.router, prefix="", tags=["health"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(chat.router, prefix="/api", tags=['chat'])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(auxiliar.router, prefix="/api", tags=["examples"])

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app", 
        host="0.0.0.0",
        port=8000, 
        reload=settings.environment == "development",
    )
   