"""
Review SQL and API Tables
"""

# SQL Alchemy
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

# Pydantic
from pydantic import BaseModel, field_validator

# Types
from datetime import date
import numpy as np

Base = declarative_base()


class ReviewRecord(BaseModel):
    date: date
    rating: int
    review_title: str | None
    review_content: str | None

    @field_validator("review_title", "review_content", mode="before")
    @classmethod
    def handle_nan(cls, v):
        if v is None:
            return None

        # handle numpy/pandas missing
        if isinstance(v, float) and np.isnan(v):
            return None

        # handle string-based missing values (THIS is your bug)
        if isinstance(v, str) and v.strip().upper() in {"NA", "N/A", "NONE", ""}:
            return None

        return v


class Review_Schema_DDBB(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=False)
    review_title = Column(String(255))
    review_content = Column(String(1023))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self):
        return (
            f"<Review(id={self.id}, date='{self.date}', rating={self.rating})>"
        )