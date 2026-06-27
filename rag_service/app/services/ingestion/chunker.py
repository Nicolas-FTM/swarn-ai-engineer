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

# Project Imports
from shared.config.loader import load_agents

# ============================================================================
# Constants
# ============================================================================
chunker_config = load_agents().get("chunker", None)

# Separators ordered to respect headers and paragraphs before raw splitting
CHUNK_SEPARATORS = ["\n## ", "\n# ", "\n\n", "\n", ". ", " "]

# ============================================================================
# Services
# ============================================================================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunker_config.get("size", None),
    chunk_overlap=chunker_config.get("overlap", None),
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