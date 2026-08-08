"""
ingest.py

Admin-only proxy endpoints to trigger and inspect rag_service ingestion.

This module provides endpoints for:
- Triggering the ingestion pipeline on rag_service
- Checking ingestion status on rag_service

Example:
    POST /admin/rag/ingest/run
"""
# ============================================================================
# Packages
# ============================================================================
# HTTP Client
import httpx

# FastAPI
from fastapi import APIRouter, Depends, HTTPException

# Project Imports
from shared.config.settings import settings
from backend.app.services.auth import require_admin

# ============================================================================
# Constants
# ============================================================================
router = APIRouter(
        prefix="/admin/rag/ingest",
        tags=["admin-rag"])

# ============================================================================
# Endpoints
# ============================================================================
@router.post("/run")
async def trigger_ingestion(_: None = Depends(require_admin)) -> dict:
    """Trigger the ingestion pipeline on rag_service. Admin role only."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.rag_service_url}/ingest/run",
            timeout=300.0,
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="rag_service ingestion failed")

    return response.json()


@router.get("/status")
async def ingestion_status(_: None = Depends(require_admin)) -> dict:
    """Check ingestion status on rag_service. Admin role only."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.rag_service_url}/ingest/status",
            timeout=30.0,
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="rag_service status check failed")

    return response.json()