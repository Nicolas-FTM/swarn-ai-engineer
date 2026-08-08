# Document Schemas for no duplication between frontend and backend services

from pydantic import BaseModel, Field

class DocumentResponse(BaseModel):
    """Document response schema."""

    id: str
    filename: str
    size: int
    status: str
