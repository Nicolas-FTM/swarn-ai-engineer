"""
evaluate.py

Admin-only endpoint to trigger on-demand Ragas evaluation over recent traces.

This module provides endpoints for:
- Running an on-demand online evaluation sample

Example:
    POST /admin/rag/evaluate/online?limit=20
"""

# ============================================================================
# Packages
# ============================================================================
# FastAPI
from fastapi import APIRouter, Depends

# Project Imports
from backend.app.services.auth import require_admin
from backend.app.evaluation.ragas_online_runner import run_online_evaluation

# ============================================================================
# Constants
# ============================================================================
router = APIRouter(
    prefix="/admin/rag/evaluate",
    tags=["admin-rag"])

# ============================================================================
# Endpoints
# ============================================================================
@router.post("/online")
async def evaluate_online(limit: int = 20, _: None = Depends(require_admin)) -> dict:
    """Trigger an on-demand Ragas evaluation over recent real traces."""
    return run_online_evaluation(limit=limit)