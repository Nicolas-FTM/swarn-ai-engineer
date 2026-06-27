"""
qdrant_uploader.py

Qdrant collection management and vector upsert utilities.

This module provides functions for:
- Ensuring a Qdrant collection exists with the right vector size
- Resolving allowed roles for a given collection
- Upserting chunk embeddings with role-based metadata

Example:
    upsert_chunks("recipes_procedures", chunks, embeddings)
"""

# ============================================================================
# Packages
# ============================================================================
# Qdrant Client
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# LangChain Documents
from langchain_core.documents import Document

# Project Imports
from shared.config.settings import settings
from shared.schemas.role import ROLE_TO_QDRANT_COLLECTIONS
from rag_service.app.services.ingestion.embedder import EMBEDDING_VECTOR_SIZE

# ============================================================================
# Constants
# ============================================================================
client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

# ============================================================================
# Helpers
# ============================================================================
def ensure_collection(collection_name: str) -> None:
    """Create a Qdrant collection if it does not already exist.

    Args:
        collection_name: Name of the collection to ensure.
    """
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=EMBEDDING_VECTOR_SIZE, distance=Distance.COSINE),
        )


def _allowed_roles_for_collection(collection_name: str) -> list[str]:
    """Resolve which roles are allowed to access a given collection.

    Args:
        collection_name: Name of the Qdrant collection.

    Returns:
        A list of role values allowed to query this collection.
    """
    # Invert ROLE_TO_QDRANT_COLLECTIONS to get collection -> roles
    return [
        role.value
        for role, collections in ROLE_TO_QDRANT_COLLECTIONS.items()
        if collection_name in collections
    ]

# ============================================================================
# Services
# ============================================================================
def upsert_chunks(collection_name: str, chunks: list[Document], embeddings: list[list[float]]) -> None:
    """Upsert chunk embeddings into a Qdrant collection with role metadata.

    Args:
        collection_name: Target Qdrant collection name.
        chunks: List of chunked Document objects.
        embeddings: List of embedding vectors, aligned with chunks.
    """
    ensure_collection(collection_name)
    allowed_roles = _allowed_roles_for_collection(collection_name)

    points = [
        PointStruct(
            id=chunk.metadata["chunk_id"].__hash__() & 0x7FFFFFFF,
            vector=embedding,
            payload={
                "domain": collection_name,
                "allowed_roles": allowed_roles,
                "source": chunk.metadata.get("source_file"),
                "doc_id": chunk.metadata.get("doc_id"),
                "chunk_id": chunk.metadata.get("chunk_id"),
                "text": chunk.page_content,
            },
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    client.upsert(collection_name=collection_name, points=points)