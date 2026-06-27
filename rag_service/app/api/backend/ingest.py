"""
ingest.py

API endpoints for triggering and inspecting the ingestion pipeline.

This module provides endpoints for:
- Running the full ingestion pipeline
- Reporting pending/processed/failed file counts per collection

Example:
    GET /ingest/status
"""

# ============================================================================
# Packages
# ============================================================================
# System
from pathlib import Path

# FastAPI
from fastapi import APIRouter

# Project Imports
from app.services.ingestion.runner import run_ingestion, DATA_ROOT

# ============================================================================
# Constants
# ============================================================================
router = APIRouter(
            prefix="/ingest",
            tags=["ingest"]
        )

# ============================================================================
# Endpoints
# ============================================================================
@router.post("/run")
async def ingest() -> dict:
    """Trigger the full ingestion pipeline across all collections."""
    summary = run_ingestion()
    return {"status": "completed", "chunks_per_collection": summary}


@router.get("/status")
async def ingest_status() -> dict:
    """Report file counts per collection, across pending/processed/failed."""
    status: dict[str, dict[str, int]] = {}

    for collection_dir in DATA_ROOT.iterdir():
        if not collection_dir.is_dir():
            continue

        if collection_dir.name == "failed":
            # 'failed' is a flat root with one subfolder per collection,
            # not a collection itself - handled separately below.
            continue

        collection_name = collection_dir.name
        pending_dir = collection_dir / "pending"
        processed_dir = collection_dir / "processed"

        status[collection_name] = {
            "pending": count_files(pending_dir),
            "processed": count_files(processed_dir),
            "failed": count_files(DATA_ROOT / "failed" / collection_name),
        }

    return status

# ============================================================================
# Helpers
# ============================================================================
def count_files(directory: Path) -> int:
    """Count regular files inside a directory, returning 0 if it doesn't exist.

    Args:
        directory: Path to inspect.

    Returns:
        Number of files found, or 0 if the directory does not exist.
    """
    if not directory.exists():
        return 0
    return sum(1 for f in directory.rglob("*") if f.is_file())