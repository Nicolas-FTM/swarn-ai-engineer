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
# System
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# FastAPI
from fastapi import APIRouter 

# ============================================================================
# Constants
# ============================================================================
router = APIRouter(
    prefix="/admin/rag/evaluate",
    tags=["admin-rag"])

# A dedicated process pool, isolated from uvicorn's uvloop, since ragas'
# nest_asyncio cannot patch uvloop and a separate process has no loop
# state inherited from the parent at all.
evaluation_pool = ProcessPoolExecutor(
    max_workers=1,
    mp_context=multiprocessing.get_context("spawn"),
)

# ============================================================================
# Endpoints
# ============================================================================
@router.post("/offline")
async def evaluate_offline() -> dict:
    """Trigger the offline Ragas evaluation against the golden dataset.

    Runs in a separate thread so ragas' internal nest_asyncio patching
    operates on its own fresh event loop, isolated from uvicorn's main
    loop (uvloop), which nest_asyncio cannot patch directly.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(evaluation_pool, _run_offline_evaluation_sync)


@router.post("/online")
async def evaluate_online(limit: int = 20) -> dict:
    """Trigger an on-demand Ragas evaluation over recent real traces.

    Runs in a separate thread for the same reason as the offline endpoint.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(evaluation_pool, _run_online_evaluation_sync, limit)


# ============================================================================
# Helpers
# ============================================================================
def _run_offline_evaluation_sync() -> dict:
    """Run the offline evaluation in a thread with a standard asyncio loop.

    Uvicorn installs uvloop globally via uvloop.install(), which replaces
    asyncio's default event loop policy entirely. This means even
    asyncio.new_event_loop() returns a uvloop.Loop unless we explicitly
    restore the standard policy first. ragas/nest_asyncio cannot patch
    uvloop.Loop, only the standard asyncio loop, so we must switch back
    to the default policy for this thread before creating its loop.
    """
    from backend.app.evaluation.ragas_offline_runner import run_offline_evaluation
    return run_offline_evaluation()


def _run_online_evaluation_sync(limit: int) -> dict:
    """Run the online evaluation in a thread with its own fresh event loop. 

    See _run_offline_evaluation_sync for why this explicit loop setup
    is required before importing ragas.
    """
    from backend.app.evaluation.ragas_online_runner import run_online_evaluation
    return run_online_evaluation(limit=limit)