# Health Schemas for no duplication between frontend and backend services

from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str