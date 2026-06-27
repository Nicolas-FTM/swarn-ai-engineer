"""
extractor.py

Document extraction utilities for the ingestion pipeline.

This module provides functions for:
- Dispatching file extraction based on file extension
- Loading PDF, Word, text, markdown and Excel files into LangChain Documents

Example:
    documents = extract_documents(Path("recipe.pdf"))
"""

# ============================================================================
# Packages
# ============================================================================
# System
from pathlib import Path

# LangChain Document Loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredExcelLoader,
)
from langchain_core.documents import Document

# ============================================================================
# Constants
# ============================================================================
EXTENSION_LOADERS = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
    ".xlsx": UnstructuredExcelLoader,
}

# ============================================================================
# Services
# ============================================================================
def extract_documents(file_path: Path) -> list[Document]:
    """Extract LangChain documents from a single source file.

    Args:
        file_path: Path of the file to extract content from.

    Returns:
        A list of LangChain Document objects with base metadata attached.

    Raises:
        ValueError: If the file extension is not supported.
    """
    loader_cls = EXTENSION_LOADERS.get(file_path.suffix.lower())
    
    if loader_cls is None:
        raise ValueError(f"Unsupported file extension: {file_path.suffix}")

    loader = loader_cls(str(file_path))
    docs = loader.load()

    # Attach base source metadata to every loaded document
    for doc in docs:
        doc.metadata["source_file"] = file_path.name
        doc.metadata["doc_id"] = file_path.stem

    return docs