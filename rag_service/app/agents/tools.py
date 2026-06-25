"""
Agent tools for RAG system.
"""
from langchain.tools import tool


@tool
def retrieve_from_documents(query: str) -> str:
    """
    Retrieve relevant information from documents.
    """
    # TODO: Implement Qdrant retrieval
    pass


@tool
def search_web(query: str) -> str:
    """
    Search web for additional information (optional).
    """
    # TODO: Implement web search if needed
    pass
