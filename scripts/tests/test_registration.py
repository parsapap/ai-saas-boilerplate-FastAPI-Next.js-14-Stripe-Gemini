#!/usr/bin/env python3
"""Test user registration endpoint"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.crud import user as crud_user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def test_registration():
    """Test creating a user"""
    print("Testing user registration...")
    
    # Create test user data
    user_data = UserCreate(
        email="testuser@example.com",
        password="TestPassword123!",
        full_name="Test User"
    )
    
    async with async_session_maker() as db:
        try:
            # Check if user exists
            existing_user = await crud_user.get_user_by_email(db, email=user_data.email)
            if existing_user:
                print(f"✓ User already exists: {existing_user.email}")
                print(f"  ID: {existing_user.id}")
                print(f"  Full Name: {existing_user.full_name}")
                print(f"  Active: {existing_user.is_active}")
                return
            
            # Create user
            print(f"Creating user: {user_data.email}")
            user = await crud_user.create_user(db, user_in=user_data)
            print(f"✓ User created successfully!")
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Full Name: {user.full_name}")
            print(f"  Active: {user.is_active}")
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_registration())
