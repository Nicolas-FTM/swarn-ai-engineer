"""
tools.py

LangGraph-facing tool wrappers around rag_service calls.

This module provides functions for:
- Closing over the resolved role so the LLM never controls it
- Exposing simple callables for use inside graph nodes

Example:
    vector_tool = build_vector_tool(role="baker")
    chunks = vector_tool("how do I make bread?")
"""

# ============================================================================
# Packages
# ============================================================================
# Typing
from typing import Callable

# Project Imports
from backend.app.services.rag_service import retrieve_vector, retrieve_sql

# ============================================================================
# Services
# ============================================================================
def build_vector_tool(role: str) -> Callable[[str], tuple[list[str], list[str]]]:
    """Build a vector retrieval tool closed over a fixed, trusted role.

    Args:
        role: Role of the requesting user, resolved upstream from JWT.

    Returns:
        A callable that takes only a query string; role is never exposed
        to the LLM as a parameter it could control.
    """
    def tool(query: str) -> tuple[list[str], list[str]]:
        return retrieve_vector(role=role, query=query)

    return tool


def build_sql_tool(role: str) -> Callable[[str], tuple[list[dict], str]]:
    """Build a SQL retrieval tool closed over a fixed, trusted role.

    Args:
        role: Role of the requesting user, resolved upstream from JWT.

    Returns:
        A callable that takes only a query string; role is never exposed
        to the LLM as a parameter it could control.
    """
    def tool(query: str) -> tuple[list[dict], str]:
        return retrieve_sql(role=role, query=query)

    return tool