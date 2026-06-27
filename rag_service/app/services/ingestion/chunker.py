"""
chunker.py

Document chunking utilities for the ingestion pipeline.

This module provides functions for:
- Splitting documents into structure-aware chunks
- Assigning stable chunk identifiers for downstream storage

Example:
    chunks = chunk_documents(documents)
"""

# ============================================================================
# Packages
# ============================================================================
# LangChain Text Splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# ============================================================================
# Constants
# ============================================================================
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

# Separators ordered to respect headers and paragraphs before raw splitting
CHUNK_SEPARATORS = ["\n## ", "\n# ", "\n\n", "\n", ". ", " "]

# ============================================================================
# Services
# ============================================================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=CHUNK_SEPARATORS,
)

def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into smaller, structure-aware chunks.

    Args:
        documents: List of LangChain Document objects to split.

    Returns:
        A list of chunked Document objects, each with a stable chunk_id.
    """
    chunks = splitter.split_documents(documents)

    # Assign a stable, human-readable chunk identifier
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{chunk.metadata['doc_id']}#{i}"

    return chunks