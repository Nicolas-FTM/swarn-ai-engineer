"""
Chat API Tables 
"""

# Pydantic
from pydantic import BaseModel

# Shared Imports
from shared.schemas.role import RoleEnum

class ChatMessage(BaseModel):
    """Chat message schema."""

    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request schema."""

    role: RoleEnum
    query: str
    session_id: str # LangGraph Thread ID


class ChatResponse(BaseModel):
    """Chat response schema."""

    answer: str
    sources: list = []
    route_used: str  # "vector_rag" | "sql_agent" | "denied" | etc.
    session_id: str # LangGraph Thread ID
    