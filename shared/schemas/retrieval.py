# Retrieval Schemas for no duplication between agents (backend) and RAG service

from pydantic import BaseModel, Field

class RetrievalRequest(BaseModel):
    query: str
    session_id: str
    user_id: str | None = None

class RetrievalResponse(BaseModel):
    answer: str
    sources: list[str] = []
    session_id: str