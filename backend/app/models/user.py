from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    baker = "baker"  # Bakers in the workshop
    sales = "sales"  # Sales Department
    hr = "hr"  # Human Resources
    cofounder = "cofounder"  # Company Co-founder
    admin = "admin"  # Admin role for system management

class User_Schema_DDBB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', hashed_password='{self.hashed_password}', full_name='{self.full_name}', role='{self.role}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"