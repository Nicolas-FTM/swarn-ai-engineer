"""
rag_service.py

HTTP client wrappers around rag_service retrieval endpoints.

This module provides functions for:
- Calling /retrieve/vector and /retrieve/sql on rag_service

Example:
    chunks, sources = retrieve_vector(role="baker", query="bread recipe")
"""
# ============================================================================
# Packages
# ============================================================================
# HTTP Client
import httpx

# Project Imports
from shared.config.settings import settings
from shared.config.loader import load_agents
from shared.observability.telemetry import traced_span

# Logger
import logging
logger = logging.getLogger(__name__)

retrieval_vector_conf = load_agents().get("retrieval", None)

# ============================================================================
# Exceptions
# ============================================================================
class RetrievalError(Exception):
    """Raised when a call to rag_service fails or is rejected."""

# ============================================================================
# Services
# ============================================================================
@traced_span()
def retrieve_vector(role: str, query: str, top_k: int = retrieval_vector_conf.get("top_k")) -> tuple[list[str], list[str]]:
    """Call rag_service's /retrieve/vector endpoint.

    Args:
        role: Role of the requesting user, resolved upstream from JWT.
        query: Natural language query to search for.
        top_k: Maximum number of chunks to retrieve.

    Returns:
        A tuple of (list of chunk texts, list of source identifiers).

    Raises:
        RetrievalError: If rag_service rejects or fails the request.
    """

    response = httpx.post(
        f"{settings.rag_service_url}/retrieve/vector",
        json={"role": role, "query": query, "top_k": top_k},
        timeout=300.0,
    )

    if response.status_code != 200:
        raise RetrievalError(f"Vector retrieval failed: {response.text}")

    payload = response.json()
    texts = [chunk["text"] for chunk in payload["chunks"]]
    sources = [chunk["source"] for chunk in payload["chunks"]]
    return texts, sources

@traced_span()
def retrieve_sql(role: str, query: str) -> tuple[list[dict], str]:
    """Call rag_service's /retrieve/sql endpoint.

    Args:
        role: Role of the requesting user, resolved upstream from JWT.
        query: Natural language question about tabular data.

    Returns:
        A tuple of (result rows, generated SQL string).

    Raises:
        RetrievalError: If rag_service rejects or fails the request.
    """

    response = httpx.post(
        f"{settings.rag_service_url}/retrieve/sql",
        json={"role": role, "query": query},
        timeout=300.0,
    )

    if response.status_code != 200:
        raise RetrievalError(f"SQL retrieval failed: {response.text}")

    payload = response.json()
    return payload["rows"], payload["generated_sql"] 