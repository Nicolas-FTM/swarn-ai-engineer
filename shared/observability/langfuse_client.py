"""
langfuse_client.py

Shared Langfuse client and callback handler factory.

This module provides functions for:
- Initializing a single configured Langfuse client
- Providing a reusable Langfuse CallbackHandler for LangChain/LangGraph

Example:
    client = get_langfuse_client()
    handler = get_langfuse_handler()
"""
# ============================================================================
# Packages
# ============================================================================
# System
import os

# Langfuse
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

# Project Imports
from shared.config.settings import settings

# ============================================================================
# Constants
# ============================================================================
_langfuse_instance: Langfuse | None = None
_langfuse_handler: CallbackHandler | None = None

# ============================================================================
# Services
# ============================================================================
def get_langfuse_client() -> Langfuse:
    """Return a singleton Langfuse client configured from environment variables.

    Both backend and rag_service must define LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY and LANGFUSE_HOST in their respective .env files.

    Returns:
        A configured Langfuse client instance, reused across calls.
    """
    global _langfuse_instance

    if _langfuse_instance is None:
        _langfuse_instance = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_url,
        )

    return _langfuse_instance


def get_langfuse_handler(session_id: str | None = None) -> CallbackHandler:
    """Return a singleton Langfuse CallbackHandler for LangChain/LangGraph.

    Returns:
        A configured CallbackHandler instance, reused across calls.
    """
    global _langfuse_handler

    if _langfuse_handler is None:
        _langfuse_handler = CallbackHandler(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_url,
        session_id=session_id
    )

    return _langfuse_handler