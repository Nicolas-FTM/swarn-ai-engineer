"""
Script to seed the database with initial users for the application.

This script creates: 1. One admin user (cofounder role) with full access
2. One sales user (sales role) with customer access
3. One baker user (baker role) with workshop access
4. One HR user (hr role) with HR access
"""

# DDBB interaction
from shared.utils.postgres import create

# Data Schema
from shared.schemas.user import User_Schema_DDBB

# Hash Passwords
from backend.app.services.auth import get_password_hash

# Logger
import logging

logger = logging.getLogger(__name__)

def create_users() -> None:
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

    for user_data in users_data:
        user_record = User_Schema_DDBB(
            username = user_data["username"],
            email = user_data["email"],
            hashed_password = get_password_hash(user_data["password"]),
            full_name = user_data["full_name"],
            role = user_data["role"]
        ) 

        flag = create(model=User_Schema_DDBB,
            instance=user_record,
            unique_filters={
                "username": user_record.username
            }
        )

        if not flag:
            # logger.info(f"Record {i} not inserted: {user.date}")
            pass

def main() -> None:
    """Main function to execute the seeding."""
    try:
        logger.info("Seeding users...")
        create_users()
        logger.info(f"Successfully created users")
    except Exception as e:
        logger.error(f"Error seeding users: {e}")

if __name__ == "__main__":
    main()     