"""
retrieve.py

API endpoints for role-aware retrieval (vector and SQL).

This module provides endpoints for:
- Vector-based document retrieval
- SQL-based tabular retrieval

Example:
    POST /retrieve/vector {"role": "baker", "query": "bread recipe"}
"""

# ============================================================================
# Packages
# ============================================================================
# FastAPI
from fastapi import APIRouter, HTTPException

# Project Imports
from shared.schemas.retrieval import (
    RetrieveVectorRequest,
    RetrieveVectorResponse,
    RetrieveSQLRequest,
    RetrieveSQLResponse,
)
from rag_service.app.services.retrieval.vector_store import (
    retrieve_from_vector_store,
    RoleNotAuthorizedInQdrantError as VectorRoleNotAuthorizedError,
)
from rag_service.app.services.retrieval.sql_agent import (
    retrieve_from_sql,
    RoleNotAuthorizedInSQLError as SQLRoleNotAuthorizedError,
    UnsafeQueryError,
)

# ============================================================================
# Constants
# ============================================================================
router = APIRouter(
    prefix="/retrieve",
    tags=["retrieve"]
)

# ============================================================================
# Endpoints
# ============================================================================
@router.post("/vector", response_model=RetrieveVectorResponse)
async def retrieve_vector(request: RetrieveVectorRequest) -> RetrieveVectorResponse:
    """Retrieve relevant document chunks for a given role and query."""
    try:
        chunks = retrieve_from_vector_store(request.role, request.query, request.top_k)
    except VectorRoleNotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return RetrieveVectorResponse(chunks=chunks)

@router.post("/sql", response_model=RetrieveSQLResponse)
async def retrieve_sql(request: RetrieveSQLRequest) -> RetrieveSQLResponse:
    """Retrieve tabular data for a given role and natural language query."""
    try:
        rows, generated_sql = retrieve_from_sql(request.role, request.query)
    except SQLRoleNotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except UnsafeQueryError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RetrieveSQLResponse(rows=rows, generated_sql=generated_sql)