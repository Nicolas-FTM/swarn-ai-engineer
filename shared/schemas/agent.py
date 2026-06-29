"""
agent.py

Shared state definition for Agents.

This module provides:
- The SQLAgentState TypedDict passed between graph nodes
"""
# ============================================================================
# Packages
# ============================================================================
# Typing
from typing import TypedDict

# ============================================================================
# Data Models
# ============================================================================
class SQLAgentState(TypedDict):
    """State passed between nodes of the SQL generation graph.

    Attributes:
        question: Natural language question from the user.
        role: Role of the requesting user, as a string value.
        generated_sql: SQL query produced by the LLM node.
        rows: Result rows produced by the execution node.
        error: Error message, set if any node fails validation/execution.
    """
    question: str
    role: str
    generated_sql: str
    rows: list[dict]
    error: str | None