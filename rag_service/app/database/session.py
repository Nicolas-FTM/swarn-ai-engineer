# Types 
from typing import Any, List

# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Variables
from shared.config import settings

# Data Models
from shared.schemas.sale import SaleRecord, Sale_Schema_DDBB
from shared.schemas.review import ReviewRecord, Review_Schema_DDBB

# Session Stream
from contextlib import contextmanager

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
@contextmanager
def get_db():
    """Initialize DDBB."""
    # DDBB Session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_sale(sale: Sale_Schema_DDBB) -> bool:
    """Add a sale."""
    with get_db() as db:
        try:
            # Check if sale already exists
            existing_sale = db.query(Sale_Schema_DDBB).filter(Sale_Schema_DDBB.order_id == sale.order_id).first()

            if existing_sale:
                # logger.info(f"Sale {sale.order_id} already exists, skipping...")
                return False

            db.add(sale)
            db.commit()
            db.refresh(sale)    
            logger.info(f"Created sale: Sale {sale.order_id}")

        except Exception as e:
            logger.error(f"There was a problem in the connection with the DDBB: {e}")

    return True

def add_review(review: Review_Schema_DDBB) -> bool:
    """Add a review."""
    with get_db() as db:
        try:
            # Check if review already exists
            existing_review = db.query(Review_Schema_DDBB).filter(Review_Schema_DDBB.date == review.date,
                                                                  Review_Schema_DDBB.rating == review.rating,
                                                                  Review_Schema_DDBB.review_title == review.review_title,
                                                                  Review_Schema_DDBB.review_content == review.review_content).first()

            if existing_review:
                # logger.info(f"Review {review.date} with {review.rating} already exists, skipping...")
                return False

            db.add(review)
            db.commit()
            db.refresh(review)    
            # logger.info(f"Created review: Review {review.date} with {review.rating}")

        except Exception as e:
            logger.error(f"There was a problem in the connection with the DDBB: {e}")

    return True


