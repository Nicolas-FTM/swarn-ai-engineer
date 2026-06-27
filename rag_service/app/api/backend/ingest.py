"""
ingest.py

Executable of the RAG model.

This module provides:
- Ingest of the RAG

Example:
    rag_response = ingest()
"""

# ============================================================================
# Packages
# ============================================================================
# FastAPI
from fastapi import APIRouter

# Project Imports
from rag_service.app.services.ingestion.runner import run_ingestion

router = APIRouter(
    prefix="/ingest",
    tags=["ingest"]
)


@router.post("/run")
async def ingest() -> dict:
    summary = run_ingestion()
    return {"status": "completed", "chunks_per_collection": summary}