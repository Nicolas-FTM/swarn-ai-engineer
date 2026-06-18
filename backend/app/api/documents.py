"""
Document upload and management endpoints.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class DocumentResponse(BaseModel):
    """Document response schema."""

    id: str
    filename: str
    size: int
    status: str


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for ingestion into the vector database.
    """
    # TODO: Implement document upload and ingestion
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Document upload not yet implemented",
    )


@router.get("/list")
async def list_documents():
    """
    List all uploaded documents.
    """
    # TODO: Implement list documents
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="List documents not yet implemented",
    )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document from the database and vector store.
    """
    # TODO: Implement delete document
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Delete document not yet implemented",
    )
