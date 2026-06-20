"""
Health check endpoints.
"""
from fastapi import APIRouter
from shared.schemas.health import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", version="0.1.0")
