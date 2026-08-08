"""
input.py

Input validation and sanitization for incoming retrieval queries.

This module provides functions for:
- Detecting basic prompt injection patterns
- Enforcing query length limits
- Rejecting empty or malformed queries

Example:
    validate_query("how do I make bread?")
"""

# ============================================================================
# Packages
# ============================================================================
# Regex
import re

# ============================================================================
# Exceptions
# ============================================================================
class InvalidQueryError(Exception):
    """Raised when a query fails input validation."""

# ============================================================================
# Constants
# ============================================================================
MAX_QUERY_LENGTH = 1000

# Lightweight pattern list for common prompt injection attempts.
# This is a first line of defense, not a replacement for role-based isolation.
INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"you are now",
    r"system prompt",
    r"act as (an? )?admin",
    r"reveal (your|the) (prompt|instructions)",
]

# ============================================================================
# Services
# ============================================================================
def validate_query(query: str) -> str:
    """Validate and normalize an incoming retrieval query.

    Args:
        query: Raw query string received from backend.

    Returns:
        The stripped, validated query string.

    Raises:
        InvalidQueryError: If the query is empty, too long, or matches a
            known prompt injection pattern.
    """
    cleaned_query = query.strip()

    if not cleaned_query:
        raise InvalidQueryError("Query cannot be empty")

    if len(cleaned_query) > MAX_QUERY_LENGTH:
        raise InvalidQueryError(f"Query exceeds max length of {MAX_QUERY_LENGTH} characters")

    lowered = cleaned_query.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            raise InvalidQueryError("Query rejected by injection guardrail")

    return cleaned_query