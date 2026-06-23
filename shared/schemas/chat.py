# Chat Schemas for no duplication between frontend and backend services

from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    """Chat message schema."""

    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request schema."""

    message: str
    session_id: str = ""


class ChatResponse(BaseModel):
    """Chat response schema."""

    message: str
    session_id: str
    
    sources: list = []