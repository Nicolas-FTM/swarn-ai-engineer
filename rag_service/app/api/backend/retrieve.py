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

# Langfuse
from langfuse.decorators import observe

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

# Logger
import logging
logger = logging.getLogger(__name__)

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
@observe(name="rag_service/retrieve_vector_endpoint")
async def retrieve_vector(request: RetrieveVectorRequest) -> RetrieveVectorResponse:
    """Retrieve relevant document chunks for a given role and query."""
    try:
        chunks = retrieve_from_vector_store(request.role, request.query, request.top_k)
    except VectorRoleNotAuthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {e}")

    return RetrieveVectorResponse(chunks=chunks)

@router.post("/sql", response_model=RetrieveSQLResponse)
@observe(name="rag_service/retrieve_sql_endpoint")
async def retrieve_sql(request: RetrieveSQLRequest) -> RetrieveSQLResponse:
    """Retrieve tabular data for a given role and natural language query."""
    try:
        rows, generated_sql = retrieve_from_sql(request.role, request.query)
    except SQLRoleNotAuthorizedError as e:
        logger.error(f"User with no role: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    except UnsafeQueryError as e:
        logger.error(f"Unsafe error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {e}")

    return RetrieveSQLResponse(rows=rows, generated_sql=generated_sql)