# Users Schemas for no duplication between agents (backend) and RAG service

from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    email: str
    username: str
    role: str

    class Config:
        from_attributes = True
