"""
Chat endpoints for conversational RAG.
"""
from fastapi import APIRouter, HTTPException, status
from shared.schemas.chat import ChatRequest, ChatResponse
from shared.schemas.agent import AgentState
from backend.app.agents.graph import agent_graph
import logging

# Definition of the router
router = APIRouter(
    prefix="/api/backend",
    tags=["chat"]
)
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    try:
        logger.info(f"Sending '{request.message}' to Agent")

        state = AgentState(query=request.message,
                           session_id=request.session_id,
                           message="",
                           sources=[])

        result = await agent_graph.ainvoke(state)
    except Exception as exc:
    # TODO: In prod, this should log with your telemetry.py
        logger.exception("Error invoking agent graph")
        raise HTTPException(
            status_code=502,
            detail="Error contacting to RAG Service"
        )

    return ChatResponse(
        message=result["message"],
        sources=result["sources"],
        session_id=request.session_id,
    )
