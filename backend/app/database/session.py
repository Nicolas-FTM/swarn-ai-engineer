# FastAPI imports
from fastapi import HTTPException

# Tipados 
from typing import Any, List

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Variables
from shared.config import settings

# Data Models
from backend.app.models.user import User_Schema_DDBB

# Logger
import logging
logger = logging.getLogger(__name__)

# Create engine using settings from shared.config
engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,  # Ensure connections are valid before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    pool_size=10,        # Maximum number of connections
    max_overflow=20      # Maximum number of connections after pool is full
)

# Create session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DDBB Session
db = SessionLocal()

# Dependency to get DB session in routes
def get_db():
    """Initialize DDBB."""

    try:
        yield db
    finally:
        db.close()

def list_users() -> List[Any]:
    """Display information from the users table."""

    users = db.query(User_Schema_DDBB).all()

    if not users:
        logger.error("No users found in the database.")
        return

    logger.info(f"Found {len(users)} user(s):")
    logger.info(f"\n{'ID':<5} {'Username':<15} {'Email':<25} {'Full Name':<20} {'Role':<10}")
    logger.info("-" * 80)

    for user in users:
        logger.info(
            f"{user.id:<5} {user.username:<15} {user.email:<25} "
            f"{user.full_name:<20} {user.role:<10}"
        )

    logger.info("-" * 80)

    return users

def get_user(id: str) -> User_Schema_DDBB:
    """Get a user by id."""
    user = db.query(User_Schema_DDBB).filter(User_Schema_DDBB.id == id).first()
    if user is None:
        raise HTTPException(status_code=401, detail=f"User not found by id: {id}")
    return user

def get_user_username(username: str) -> User_Schema_DDBB:
    """Get a user by username."""
    user = db.query(User_Schema_DDBB).filter(User_Schema_DDBB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail=f"User not found by username: {id}")
    return user
