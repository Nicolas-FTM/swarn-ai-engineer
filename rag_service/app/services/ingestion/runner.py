"""
runner.py
Ingestion pipeline orchestrator for unstructured documents.
This module provides functions for:
- Restoring files from 'processed'/'failed' back to 'raw' before each run
- Walking raw documents per Qdrant collection
- Extracting, chunking and embedding content
- Uploading vectors to Qdrant
- Moving processed/failed files for traceability
Example:
    summary = run_ingestion()
    print(summary)
"""
# ============================================================================
# Packages
# ============================================================================
# System
import shutil
from pathlib import Path

# Datetime
from datetime import datetime

# Logger
import logging

# Project Imports
from rag_service.app.services.ingestion.extractor import extract_documents
from rag_service.app.services.ingestion.chunker import chunk_documents
from rag_service.app.services.ingestion.embedder import embedding_model
from rag_service.app.services.ingestion.qdrant_uploader import upsert_chunks
from shared.observability.telemetry import traced_span

logger = logging.getLogger(__name__)

# ============================================================================
# Constants
# ============================================================================
DATA_ROOT = Path("rag_service/data")
RAW_ROOT = DATA_ROOT / "raw"
PROCESSED_ROOT = DATA_ROOT / "processed"
FAILED_ROOT = DATA_ROOT / "failed"

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".xlsx"}

# Folders under raw/ that are NOT Qdrant collections (handled by other pipelines)
EXCLUDED_RAW_FOLDERS = {"sales"}

# ============================================================================
# Helpers
# ============================================================================
@traced_span(name="embed_documents")
def embed_texts(texts: list[str]) -> list[list[float]]:
    return embedding_model.embed_documents(texts)

def restore_folder_to_raw(source_root: Path) -> None:
    """Move every file from a root folder's per-collection subfolders back to raw.

    Args:
        source_root: Root folder to restore from (PROCESSED_ROOT or FAILED_ROOT).
    """
    if not source_root.exists():
        return

    for collection_dir in source_root.iterdir():
        if not collection_dir.is_dir():
            continue

        collection_name = collection_dir.name
        raw_collection_dir = RAW_ROOT / collection_name
        raw_collection_dir.mkdir(parents=True, exist_ok=True)

        for item in collection_dir.iterdir():
            # Skip error logs explicitly; they are deleted, not restored
            if item.is_file() and item.name.endswith("_error.log"):
                continue

            if item.is_file():
                shutil.move(str(item), str(raw_collection_dir / item.name))


def clear_failed_logs() -> None:
    """Delete every '_error.log' file left under the failed/ tree."""
    if not FAILED_ROOT.exists():
        return

    for log_path in FAILED_ROOT.rglob("*_error.log"):
        log_path.unlink()


def move_to_processed(file_path: Path, collection_name: str) -> None:
    """Move a successfully ingested file to its 'processed' folder.

    Args:
        file_path: Path of the ingested file.
        collection_name: Name of the Qdrant collection the file belongs to.
    """
    processed_dir = PROCESSED_ROOT / collection_name
    processed_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(processed_dir / file_path.name))


def move_to_failed(file_path: Path, collection_name: str, error: Exception) -> None:
    """Move a failed file to the 'failed' folder and log the error.

    Args:
        file_path: Path of the file that failed ingestion.
        collection_name: Name of the target Qdrant collection.
        error: Exception raised during processing.
    """
    failed_dir = FAILED_ROOT / collection_name
    failed_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(failed_dir / file_path.name))

    # Store error details next to the failed file for later inspection
    log_path = failed_dir / f"{file_path.stem}_error.log"
    log_path.write_text(f"[{datetime.utcnow().isoformat()}] {error}\n")
    logger.error(f"Failed to ingest {file_path.name}: {error}")

# ============================================================================
# Services
# ============================================================================
def restore_raw_state() -> None:
    """Restore raw/ to a clean state before a new ingestion run.

    Moves every file from 'processed' and 'failed' back into their matching
    'raw' subfolder, and deletes leftover error logs from 'failed'. This
    guarantees that run_ingestion() always reprocesses the full dataset.
    """
    restore_folder_to_raw(PROCESSED_ROOT)
    restore_folder_to_raw(FAILED_ROOT)
    clear_failed_logs()


@traced_span()
def run_ingestion() -> dict:
    """Run the full ingestion pipeline for all Qdrant collections.

    Restores any previously processed/failed files back to raw, then walks
    every collection's 'raw' folder, extracts and chunks each supported
    file, embeds the chunks, and upserts them into Qdrant. Successful files
    are moved to 'processed', failed files to 'failed'.

    Returns:
        A summary dict with chunk counts and failure counts per collection.
    """
    restore_raw_state()

    summary = {"processed": {}, "failed": {}}

    for collection_dir in RAW_ROOT.iterdir():
        if not collection_dir.is_dir() or collection_dir.name in EXCLUDED_RAW_FOLDERS:
            continue

        collection_name = collection_dir.name
        chunks_uploaded = 0
        failed_count = 0

        for file_path in collection_dir.rglob("*"):
            if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                logger.info(file_path.name)

                # Extract raw documents from the source file
                documents = extract_documents(file_path)

                # Split documents into smaller, structure-aware chunks
                chunks = chunk_documents(documents)

                # Compute embeddings for every chunk
                texts = [chunk.page_content for chunk in chunks]
                # embeddings = embedding_model.embed_documents(texts)
                embeddings = embed_texts(texts)

                # Upsert chunks and their vectors into the target collection
                upsert_chunks(collection_name, chunks, embeddings)

                move_to_processed(file_path, collection_name)
                chunks_uploaded += len(chunks)

            except Exception as e:
                logger.error(e)
                move_to_failed(file_path, collection_name, e)
                failed_count += 1

        summary["processed"][collection_name] = chunks_uploaded
        summary["failed"][collection_name] = failed_count

    return summary

# ============================================================================
# Main Entry Point
# ============================================================================
def main() -> None:
    """Run the ingestion pipeline as a standalone script."""
    result = run_ingestion()
    print(result)


if __name__ == "__main__":
    main()