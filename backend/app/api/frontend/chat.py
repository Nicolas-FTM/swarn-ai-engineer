"""
chat.py

Chat endpoint exposed to the frontend.

This module provides endpoints for:
- Submitting a user question and receiving the agent's answer

Example:
    POST /chat {"query": "how do I make bread?"}
"""

# ============================================================================
# Packages
# ============================================================================
# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status

# Langfuse
from langfuse.decorators import observe

# Project Imports
from backend.app.agents.runner import run_chat
from backend.app.services.auth import get_current_user
from shared.schemas.chat import ChatRequest, ChatResponse
from shared.guardrails.output_backend import validate_response_route

# Logger
import logging
logger = logging.getLogger(__name__)

# ============================================================================
# Constants
# ============================================================================
router = APIRouter(
            prefix="/chat",
            tags=["chat"]
            )

# ============================================================================
# Endpoints
# ============================================================================
@router.post("", response_model=ChatResponse)
@observe(name="backend/chat_endpoint")
async def chat(request: ChatRequest, current_user=Depends(get_current_user)) -> ChatResponse:
    """Submit a user question and return the agent's answer.

    The role is resolved exclusively from the authenticated user's JWT,
    never from the request body, to enforce role isolation upstream of
    rag_service's own guardrails.
    """
    result, _ = run_chat(
        role=current_user.role,
        query=request.query,
        session_id=request.session_id
        )
    
    try:
        validate_response_route(current_user.role, result["route"])
    except Exception as e:
        logger.error("Malicious Prompt Injection detected")
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User with role {current_user.role} accesing to non-associated data",
            )
    
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        route_used=result["route"],
        session_id=request.session_id
    )


