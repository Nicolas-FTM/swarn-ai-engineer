"""
conftest.py

Shared pytest fixtures for rag_service tests.

This module provides fixtures for:
- Mocking the Qdrant client to avoid real network calls
- Mocking the embedding model to avoid real Ollama calls

Example:
    def test_something(mock_qdrant_client):
        ...
"""
# ============================================================================
# Packages
# ============================================================================
# Pytest
import pytest

# Unittest Mock
from unittest.mock import patch

# ============================================================================
# Fixtures
# ============================================================================
@pytest.fixture
def mock_qdrant_client():
    """Patch the Qdrant client used in vector_store.py with a mock.

    Returns:
        The mock client instance, so tests can assert on calls made to it.
    """
    with patch("rag_service.app.services.retrieval.vector_store.client") as mock_client:
        mock_client.collection_exists.return_value = True
        mock_client.query_points.return_value = []
        yield mock_client


@pytest.fixture
def mock_embedding_model():
    """Patch the embedding model used in vector_store.py with a mock.

    Returns:
        The mock embedding model instance.
    """
    with patch("rag_service.app.services.retrieval.vector_store.embedding_model") as mock_model:
        mock_model.embed_query.return_value = [0.0] * 1024
        yield mock_model


@pytest.fixture
def mock_postgres_engine():
    """Patch the SQLAlchemy engine used in sql_agent.py with a mock.

    Returns:
        The mock engine instance, so tests can assert no connection was made.
    """
    with patch("rag_service.app.services.retrieval.sql_agent.engine") as mock_engine:
        yield mock_engine