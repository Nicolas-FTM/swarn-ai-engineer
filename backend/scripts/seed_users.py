"""
Script to seed the database with initial users for the application.

This script creates: 1. One admin user (cofounder role) with full access
2. One sales user (sales role) with customer access
3. One baker user (baker role) with workshop access
4. One HR user (hr role) with HR access
"""

import sys
import os
from sqlalchemy.orm import Session

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database.session import SessionLocal
from backend.app.models.user import User_Schema_DDBB
from shared.config import settings
from backend.app.services.auth import get_password_hash

import logging

logger = logging.getLogger(__name__)

def create_users(db: Session) -> None:
    """Create initial users for the application."""
    # Define users to create   
    users_data = [
        {
            "username": "admin",
            "email": "admin@bakery.com",
            "password": "admin123456",
            "full_name": "admin",
            "role": "admin"
        },
        {
            "username": "cofounder",
            "email": "cofounder@bakery.com",
            "password": "cofounder123456",
            "full_name": "Co-Founder",
            "role": "cofounder"
        },
        {
            "username": "sales_agent",
            "password": "sales123456",
            "email": "sales@bakery.com",
            "full_name": "Sales Department",
            "role": "sales"
        },
        {
            "username": "bakery_staff",
            "email": "baker@bakery.com",
            "password": "baker123456",
            "full_name": "Head Baker",
            "role": "baker"
        },
        {
            "username": "hr_manager",
            "email": "hr@bakery.com",
            "password": "hr123456",
            "full_name": "HR Manager",
            "role": "hr"
        }
    ]

    # Create users
    created_users = []
    for user_data in users_data:
        # Check if user already exists
        existing_user = db.query(User_Schema_DDBB).filter(User_Schema_DDBB.username == user_data["username"]).first()
        if existing_user:
            logger.info(f"User {user_data['username']} already exists, skipping...")
            created_users.append(existing_user)
            continue

        # Create new user
        hashed_password = get_password_hash(user_data["password"])
        new_user = User_Schema_DDBB(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            full_name=user_data["full_name"],
            role=user_data["role"]    
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        created_users.append(new_user)
        logger.info(f"Created user: {new_user.username} with role: {new_user.role}")

    return created_users

def main() -> None:
    """Main function to execute the seeding."""
    db = SessionLocal()
    try:
        logger.info("Seeding users...")
        users = create_users(db)
        logger.info(f"Successfully created {len(users)} users")
    except Exception as e:
        logger.error(f"Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()    