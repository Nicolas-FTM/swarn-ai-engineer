"""
embedder.py

Embedding model configuration for the ingestion pipeline.

This module provides:
- A configured Ollama embedding client (mxbai-embed-large)
- A single entry point used by the ingestion runner and retrieval service

Example:
    vectors = embedding_model.embed_documents(["some chunk text"])
"""

# ============================================================================
# Packages
# ============================================================================
# LangChain Embeddings
from langchain_ollama import OllamaEmbeddings

# Project Imports
from shared.config.settings import settings

# ============================================================================
# Constants
# ============================================================================
EMBEDDING_MODEL_NAME = "mxbai-embed-large"
EMBEDDING_VECTOR_SIZE = 1024

# ============================================================================
# Services
# ============================================================================
embedding_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    base_url=settings.ollama_base_url,
)