"""
retrieval.py

Pydantic request/response models for the rag_service API.

This module provides:
- Vector retrieval request/response models
- SQL retrieval request/response models

Example:
    request = RetrieveVectorRequest(role=RoleEnum.baker, query="how to make bread")
"""

# ============================================================================
# Packages
# ============================================================================
# Pydantic
from pydantic import BaseModel

# Project Imports
from shared.schemas.role import RoleEnum
from shared.config.loader import load_agents

retrieval_vector_conf = load_agents().get("retrieval", None).get("vector", None)

# ============================================================================
# Data Models
# ============================================================================
class RetrieveVectorRequest(BaseModel):
    """Request payload for vector-based document retrieval."""
    role: RoleEnum
    query: str
    top_k: int = retrieval_vector_conf["top_k"]


class RetrievedChunk(BaseModel):
    """A single retrieved chunk with its source metadata."""
    text: str
    source: str
    chunk_id: str
    score: float


class RetrieveVectorResponse(BaseModel):
    """Response payload for vector-based document retrieval."""
    chunks: list[RetrievedChunk]


class RetrieveSQLRequest(BaseModel):
    """Request payload for SQL-based tabular retrieval."""
    role: RoleEnum
    query: str


class RetrieveSQLResponse(BaseModel):
    """Response payload for SQL-based tabular retrieval."""
    rows: list[dict]
    generated_sql: str