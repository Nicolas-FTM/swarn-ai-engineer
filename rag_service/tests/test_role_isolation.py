"""
test_role_isolation.py

Unit tests enforcing role-based isolation across vector and SQL retrieval.

This module provides tests for:
- Verifying unauthorized roles are rejected before touching Qdrant/Postgres
- Verifying authorized roles only reach their allowed collections
- Verifying the output guardrail catches cross-domain leaks

Example:
    pytest tests/test_role_isolation.py -v
"""

# ============================================================================
# Packages
# ============================================================================
# Pytest
import pytest

# Project Imports
from shared.schemas.role import RoleEnum
from shared.schemas.retrieval import RetrievedChunk
from rag_service.app.services.retrieval.vector_store import (
    retrieve_from_vector_store,
    RoleNotAuthorizedInQdrantError as VectorRoleNotAuthorizedError,
)
from rag_service.app.services.retrieval.sql_agent import (
    retrieve_from_sql,
    RoleNotAuthorizedInSQLError as SQLRoleNotAuthorizedError,
)
from shared.guardrails.output_rag_service import validate_chunks, LeakedChunkError

# ============================================================================
# Tests — Vector Retrieval Isolation
# ============================================================================
def test_sales_has_no_vector_access_at_all(mock_qdrant_client, mock_embedding_model):
    """Sales has zero vector collections allowed; must be rejected immediately."""
    with pytest.raises(VectorRoleNotAuthorizedError):
        retrieve_from_vector_store(role=RoleEnum.sales, query="any question")

    # The critical assertion: Qdrant must never be touched for an unauthorized role
    mock_qdrant_client.query_points.assert_not_called()


def test_baker_cannot_reach_confidential_collection(mock_qdrant_client, mock_embedding_model):
    """A baker's query must only search recipes_procedures, never confidential."""
    retrieve_from_vector_store(role=RoleEnum.baker, query="bread recipe")

    called_collections = [
        call.kwargs["collection_name"] for call in mock_qdrant_client.query_points.call_args_list
    ]

    assert "general_and_confidential" not in called_collections
    assert "cofounder_doc" not in called_collections
    assert all(c == "recipes_procedures" for c in called_collections)


def test_hr_cannot_reach_recipes_collection(mock_qdrant_client, mock_embedding_model):
    """An hr query must only search general_and_confidential, never recipes_procedures."""
    retrieve_from_vector_store(role=RoleEnum.hr, query="vacation policy")

    called_collections = [
        call.kwargs["collection_name"] for call in mock_qdrant_client.query_points.call_args_list
    ]

    assert "recipes_procedures" not in called_collections
    assert "cofounder_doc" not in called_collections
    assert all(c == "general_and_confidential" for c in called_collections)


def test_cofounder_cannot_reach_any_other_collection(mock_qdrant_client, mock_embedding_model):
    """A cofounder query must only search cofounder_doc."""
    retrieve_from_vector_store(role=RoleEnum.cofounder, query="expansion strategy")

    called_collections = [
        call.kwargs["collection_name"] for call in mock_qdrant_client.query_points.call_args_list
    ]

    assert called_collections == ["cofounder_doc"]


def test_admin_can_reach_all_collections(mock_qdrant_client, mock_embedding_model):
    """Admin must be the only role allowed to query every collection."""
    retrieve_from_vector_store(role=RoleEnum.admin, query="anything")

    called_collections = {
        call.kwargs["collection_name"] for call in mock_qdrant_client.query_points.call_args_list
    }

    assert called_collections == {"recipes_procedures", "general_and_confidential", "cofounder_doc"}

# ============================================================================
# Tests — SQL Retrieval Isolation
# ============================================================================
@pytest.mark.parametrize("role", [RoleEnum.baker, RoleEnum.hr, RoleEnum.cofounder])
def test_role_without_sql_access_is_rejected(role, mock_postgres_engine):
    """Roles with no SQL access must be rejected before touching Postgres."""
    with pytest.raises(SQLRoleNotAuthorizedError):
        retrieve_from_sql(role=role, query="total sales last month")

    # The critical assertion: Postgres must never be touched for an unauthorized role
    mock_postgres_engine.connect.assert_not_called()

# ============================================================================
# Tests — Output Guardrail (Defense in Depth)
# ============================================================================
def test_output_guardrail_blocks_leaked_chunk_for_baker():
    """If a confidential chunk somehow reached a baker response, it must be caught."""
    leaked_chunk = RetrievedChunk(
        text="confidential salary data",
        source="salaries.pdf",
        chunk_id="salaries#0",
        domain="general_and_confidential",
        score=0.9,
    )

    with pytest.raises(LeakedChunkError):
        validate_chunks(role=RoleEnum.baker, chunks=[leaked_chunk])


def test_output_guardrail_allows_matching_domain():
    """A chunk from the role's own allowed domain must pass through untouched."""
    valid_chunk = RetrievedChunk(
        text="bread recipe",
        source="bread.pdf",
        chunk_id="bread#0",
        domain="recipes_procedures",
        score=0.95,
    )

    result = validate_chunks(role=RoleEnum.baker, chunks=[valid_chunk])

    assert result == [valid_chunk]