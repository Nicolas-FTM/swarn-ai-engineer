"""
User SQL and API Tables 
"""

# SQL Alchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqEnum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Pydantic
from pydantic import BaseModel, EmailStr

# Imports
from shared.schemas.role import RoleEnum

Base = declarative_base()

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
    full_name: str

    class Config:
        from_attributes = True

class User_Schema_DDBB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(SqEnum(RoleEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', hashed_password='{self.hashed_password}', full_name='{self.full_name}', role='{self.role}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"