# Tipados 
from typing import Any, List

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Variables
from shared.config import settings

# Data Models
from backend.app.models.user import User

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

# Dependency to get DB session in routes
def get_db():
    """Initialize DDBB."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def list_users() -> List[Any]:
    """Display information from the users table."""

    db = SessionLocal()

    users = db.query(User).all()

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