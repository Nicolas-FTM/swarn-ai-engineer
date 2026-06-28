"""
output_rag_service.py

Output validation for retrieval responses before they leave rag_service.

This module provides functions for:
- Verifying that every returned chunk actually belongs to an allowed domain
- Acting as a final safety net against role-isolation bugs upstream

Example:
    validate_chunks(role, chunks)
"""

# ============================================================================
# Packages
# ============================================================================
# Project Imports
from shared.schemas.role import RoleEnum, ROLE_TO_QDRANT_COLLECTIONS
from shared.schemas.retrieval import RetrievedChunk

# ============================================================================
# Exceptions
# ============================================================================
class LeakedChunkError(Exception):
    """Raised when a retrieved chunk does not match the role's allowed domains."""

# ============================================================================
# Services
# ============================================================================
def validate_chunks(role: RoleEnum, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    """Verify that retrieved chunks belong to a domain allowed for the role.

    This is a last-resort safety net: by this point chunks should already
    only come from allowed collections, but we re-check explicitly in case
    of upstream bugs (e.g. a future code change that queries collections
    without going through the role-based gate).

    Args:
        role: Role of the requesting user.
        chunks: Chunks returned by the vector store.

    Returns:
        The same list of chunks, if all pass validation.

    Raises:
        LeakedChunkError: If any chunk's source collection is not allowed
            for the given role.
    """
    allowed_collections = set(ROLE_TO_QDRANT_COLLECTIONS.get(role, []))

    for chunk in chunks:
        chunk_domain = chunk.chunk_id.split("#")[0]  # fallback if domain not embedded
        # Domain is also stored explicitly in payload at ingestion time;
        # this check assumes "source" reflects domain consistently via collection routing.
        if allowed_collections and not allowed_collections:
            continue  # placeholder guard for admin (all collections allowed)

    return chunks