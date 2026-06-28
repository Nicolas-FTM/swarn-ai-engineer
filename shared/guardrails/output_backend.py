"""
output_backend.py

Final safety check on the chat response before it reaches the frontend.

This module provides functions for:
- Verifying route_used matches what the role is actually allowed to use

Example:
    validate_response(role="baker", route_used="vector_rag")
"""

# ============================================================================
# Packages
# ============================================================================
# Project Imports
from shared.schemas.role import RoleEnum, ROLE_HAS_SQL_ACCESS, ROLE_TO_QDRANT_COLLECTIONS

# ============================================================================
# Exceptions
# ============================================================================
class InvalidRouteForRoleError(Exception):
    """Raised when a response's route does not match the role's actual permissions."""

# ============================================================================
# Services
# ============================================================================
def validate_response_route(role: RoleEnum, route_used: str) -> None:
    """Verify the route used to answer is one the role is actually allowed to use.

    This is a last-resort safety net: rag_service should already have
    rejected unauthorized retrieval, but this re-checks at the backend
    boundary in case of an upstream bug.

    Args:
        role: Role of the requesting user.
        route_used: Route the graph used to answer ("vector" or "sql").

    Raises:
        InvalidRouteForRoleError: If the role is not allowed to use that route.
    """
    if route_used == "sql" and not ROLE_HAS_SQL_ACCESS.get(role, False):
        raise InvalidRouteForRoleError(f"Role '{role.value}' is not allowed to use SQL route")

    if route_used == "vector" and not ROLE_TO_QDRANT_COLLECTIONS.get(role, []):
        raise InvalidRouteForRoleError(f"Role '{role.value}' is not allowed to use vector route")