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
from shared.config.loader import load_agents
from shared.config.settings import settings

agent_config = load_agents().get("llm_embedding", None)

# ============================================================================
# Services
# ============================================================================

embedding_model = None

if agent_config.get("provider", None) == "ollama":
    embedding_model = OllamaEmbeddings(
        model=agent_config.get("model", None),
        base_url=settings.ollama_base_url,
    )

