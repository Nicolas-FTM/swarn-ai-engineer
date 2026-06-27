"""
Custom exceptions.
"""


class SwarnException(Exception):
    """Base exception for Swarn application."""

    pass


class DocumentIngestionError(SwarnException):
    """Raised when document ingestion fails."""

    pass


class RAGError(SwarnException):
    """Raised when RAG operation fails."""

    pass


class VectorStoreError(SwarnException):
    """Raised when vector store operation fails."""

    pass
