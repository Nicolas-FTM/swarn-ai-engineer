"""
vector_store.py

Role-aware vector retrieval against Qdrant collections.

This module provides functions for:
- Resolving which collections a role is allowed to query
- Embedding the incoming query
- Searching Qdrant and returning role-authorized chunks only

Example:
    chunks = retrieve_from_vector_store(RoleEnum.baker, "how to make bread")
"""

# ============================================================================
# Packages
# ============================================================================
# Qdrant Client
from qdrant_client import QdrantClient

# Project Imports
from shared.config.settings import settings
from shared.schemas.role import RoleEnum, ROLE_TO_QDRANT_COLLECTIONS
from shared.schemas.retrieval import RetrievedChunk
from rag_service.app.services.ingestion.embedder import embedding_model
from shared.observability.telemetry import traced_span

# ============================================================================
# Exceptions
# ============================================================================
class RoleNotAuthorizedInQdrantError(Exception):
    """Raised when a role has no access to any vector collection."""

# ============================================================================
# Constants
# ============================================================================
client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

# ============================================================================
# Services
# ============================================================================
@traced_span()
def retrieve_from_vector_store(role: RoleEnum, query: str, top_k: int = 5) -> list[RetrievedChunk]:
    """Retrieve relevant chunks from the collections allowed for a given role.

    Args:
        role: Role of the requesting user, resolved upstream by backend.
        query: Natural language query to search for.
        top_k: Maximum number of chunks to return per collection.

    Returns:
        A list of RetrievedChunk objects, sorted by relevance score.

    Raises:
        RoleNotAuthorizedError: If the role has no allowed collections at all.
    """
    allowed_collections = ROLE_TO_QDRANT_COLLECTIONS.get(role, [])

    # Hard stop: do not even attempt a query if the role has no vector access.
    # This enforces physical isolation instead of relying only on payload filters.
    if not allowed_collections:
        raise RoleNotAuthorizedInQdrantError(f"Role '{role.value}' has no vector store access")

    query_vector = embedding_model.embed_query(query)
    results: list[RetrievedChunk] = []

    for collection_name in allowed_collections:
        if not client.collection_exists(collection_name):
            continue

        hits = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
        )

        for hit in hits:
            results.append(
                RetrievedChunk(
                    text=hit.payload.get("text", ""),
                    source=hit.payload.get("source", ""),
                    chunk_id=hit.payload.get("chunk_id", ""),
                    score=hit.score,
                )
            )

    # Sort merged results across collections by relevance score, descending
    results.sort(key=lambda chunk: chunk.score, reverse=True)
    return results[:top_k]