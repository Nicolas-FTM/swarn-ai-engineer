"""
RAG Service FastAPI application entry point.
"""
from contextlib import asynccontextmanager
import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from rag_service.app.api import health, example, generation

from shared.utils.logging_config import JSONFormatter, setup_logging
from shared.utils.opentelemetry_init import init_telemetry
from shared.utils.metrics import init_metrics, get_metrics_app
from shared.config import settings

# Configure logging
setup_logging(level=settings.log_level)
logger = logging.getLogger("rag_service")

# Measure traces
trace_provider, resource = init_telemetry("rag_service")
init_metrics(resource)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title="RAG Service FastAPI Application",
    description="RAG Service FastAPI application with observability",
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
app.include_router(example.router, prefix="/api", tags=["examples"])
app.include_router(generation.router, prefix="/api", tags=["generation"])

if __name__ == "__main__":
    uvicorn.run(
        "rag_service.app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.environment == "development",
    )
