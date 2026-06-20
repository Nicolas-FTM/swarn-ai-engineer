"""
Chat endpoints for conversational RAG.
"""
from fastapi import APIRouter, HTTPException, status
from shared.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """
    Send a message and get a RAG-enhanced response.
    """
    # TODO: Implement RAG chat with LangGraph
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Chat endpoint not yet implemented",
    )


@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get conversation history.
    """
    # TODO: Implement get conversation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get conversation not yet implemented",
    )
