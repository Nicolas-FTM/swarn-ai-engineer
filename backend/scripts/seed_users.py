"""
Script to seed the database with initial users for the Sweet Haven Bakery application.

This script creates: 1. One admin user (cofounder role) with full access
2. One sales user (sales role) with customer access
3. One baker user (baker role) with workshop access
4. One HR user (hr role) with HR access
"""

import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from hashlib import sha256
import secrets

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.models.user import User
from app.shared.config import settings
from app.services.auth import get_password_hash

def create_users(db: Session) -> None:
    """Create initial users for the application."""
    # Define users to create
    users_data = [
        {
            "username": "cofounder",
            "email": "cofounder@sweethavenbakery.com",
            "full_name": "Sweet Haven Co-Founder",
            "role": "cofounder",
            "password": "cofounder123"
        },
        {
            "username": "sales_agent",
            "email": "sales@sweethavenbakery.com",
            "full_name": "Sales Department",
            "role": "sales",
            "password": "sales123"
        },
        {
            "username": "bakery_staff",
            "email": "baker@sweethavenbakery.com",
            "full_name": "Head Baker",
            "role": "baker",
            "password": "baker123"
        },
        {
            "username": "hr_manager",
            "email": "hr@sweethavenbakery.com",
            "full_name": "HR Manager",
            "role": "hr",
            "password": "hr123"
        }
    ]

    # Create users
    created_users = []
    for user_data in users_data:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_user:
            print(f"User {user_data['username']} already exists, skipping...")
            created_users.append(existing_user)
            continue

        # Create new user
        hashed_password = get_password_hash(user_data["password"])
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            full_name=user_data["full_name"],
            role=user_data["role"],
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        created_users.append(new_user)
        print(f"Created user: {new_user.username} with role: {new_user.role}")

    return created_users

def main() -> None:
    """Main function to execute the seeding."""
    db = SessionLocal()
    try:
        print("Seeding users...")
        users = create_users(db)
        print(f"Successfully created {len(users)} users")
    except Exception as e:
        print(f"Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()