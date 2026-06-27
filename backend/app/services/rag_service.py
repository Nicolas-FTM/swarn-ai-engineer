"""
RAG Service: Orchestrates document retrieval and LLM interaction.
"""
import logging
import httpx
from shared.schemas.chat import ChatRequest, ChatResponse
from shared.config.settings import settings

logger = logging.getLogger(__name__)

class RAGService:
    """Service for RAG operations."""

    def __init__(self):
        """Initialize RAG service."""
        # TODO: Initialize Qdrant client, Ollama client, LangGraph graph
        pass

    async def call_rag_service(message: str) -> ChatResponse:

        async with httpx.AsyncClient() as client:
            prefix="/api/generate"
            endpoint = f"{settings.rag_service_url}{prefix}" 
            logger.info(endpoint)
            resp = await client.post(
                endpoint,
                json=ChatRequest(message=message).model_dump(),
                timeout=30.0,
            )
            resp.raise_for_status()
            return ChatResponse(**resp.json())

    async def retrieve_documents(self, query: str, top_k: int = 5):
        """
        Retrieve relevant documents from vector store.
        """
        # TODO: Implement retrieval from Qdrant
        pass

    async def generate_response(self, query: str, context: str):
        """
        Generate response using LLM with retrieved context.
        """
        # TODO: Implement LLM call via Ollama + LangGraph
        pass

    async def ingest_document(self, filepath: str):
        """
        Ingest document: chunk, embed, store in Qdrant.
        """
        # TODO: Implement document ingestion pipeline
        pass
