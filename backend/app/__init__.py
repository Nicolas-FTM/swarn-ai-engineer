# Agents
from .agents.graph import create_rag_graph
from .agents.tools import retrieve_from_documents, search_web

# API
from .api.health import HealthResponse, health_check
from .api.users import (
    register_user,
    login,
    get_current_user,
)
from .api.chat import (
    chat_message,
    get_conversation,
)
from .api.documents import (
    upload_document,
    list_documents,
    delete_document,
)
from .api.example import (
    retrieve_all,
    retrieve_user
)

# Services
from .services.rag_service import RAGService

# Utils
from .utils.exceptions import (
    SwarnException,
    DocumentIngestionError,
    RAGError,
    VectorStoreError,
)

from .utils.telemetry import setup_observability

__all__ = [
    # Agents
    "create_rag_graph",
    "retrieve_from_documents",
    "search_web",

    # Health
    "HealthResponse",
    "health_check",

    # Users
    "register_user",
    "login",
    "get_current_user",

    # Chat
    "chat_message",
    "get_conversation",

    # Documents
    "upload_document",
    "list_documents",
    "delete_document",
    
    # Example
    "retrieve_user",
    "retrieve_all"

    # Services
    "RAGService",

    # Exceptions
    "SwarnException",
    "DocumentIngestionError",
    "RAGError",
    "VectorStoreError",

    # Telemetry
    "setup_observability",
]