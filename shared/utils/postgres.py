"""
postgres.py

PostgreSQL connection and generic CRUD utilities.

This module provides:
- SQLAlchemy engine initialization
- Database session management
- Generic create operations with duplicate validation
"""

# ============================================================================
# Packages
# ============================================================================
# Types
from typing import Any, Type

# Context Managers
from contextlib import contextmanager

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Project Imports
from shared.config import settings

# Logger
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# Database Configuration
# ============================================================================
engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ============================================================================
# Database Session
# ============================================================================
@contextmanager
def get_db():
    """
    Create and close a database session.

    Yields:
        Active SQLAlchemy session.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================================
# CRUD Operations
# ============================================================================

# Create
def create(
    model: Type[DeclarativeBase],
    instance: DeclarativeBase,
    unique_filters: dict[str, Any] | None = None,
) -> bool:
    """
    Create a new database record.

    Args:
        model:
            SQLAlchemy model class.

        instance:
            SQLAlchemy model instance to persist.

        unique_filters:
            Optional filters used to check whether the record
            already exists.

    Returns:
        True if the record was created successfully,
        False otherwise.
    """
    with get_db() as db:

        try:

            if unique_filters:

                existing_record = (
                    db.query(model)
                    .filter_by(**unique_filters)
                    .first()
                )

                if existing_record:
                    return False

            db.add(instance)
            db.commit()
            db.refresh(instance)

            logger.info(
                "Created %s",
                model.__name__,
            )

            return True

        except Exception as error:

            db.rollback()

            logger.exception(
                "Database error while creating %s: %s",
                model.__name__,
                error,
            )

            return False
        
# Read
def get(
    model: Type[DeclarativeBase],
    filters: dict[str, Any] | None = None,
    first: bool = True,
) -> list[DeclarativeBase] | DeclarativeBase | None:
    """
    Retrieve records from the database.

    Args:
        model:
            SQLAlchemy model class.

        filters:
            Optional dictionary of filters applied using filter_by.

        first:
            If True, returns only the first matching record.

    Returns:
        A list of records, a single record, or None.
    """
    with get_db() as db:

        try:
            query = db.query(model)

            if filters:
                query = query.filter_by(**filters)

            if first:
                return query.first()

            return query.all()

        except Exception as error:

            logger.exception(
                "Database error while querying %s: %s",
                model.__name__,
                error,
            )

            return None