# FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# SQL Alchemy
from sqlalchemy.orm import Session

# Datetime
from datetime import timedelta

# Authentication functions
from backend.app.services.auth import (
    authenticate_user,
    decode_access_token,
    create_access_token,
    get_current_user,
    verify_password,
    oauth2_scheme
)
# DDBB Connection
from backend.app.database.session import get_db, get_user_username
# Use models
from backend.app.models.user import User_Schema_DDBB
from backend.app.models.auth import LoginRequest, TokenResponse

# Environment variables
from shared.config import settings

# Models
from shared.schemas.users import UserResponse

# Definition of the router
router = APIRouter(
    prefix="/api/backend",
    tags=["auth"]
)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    """Login for the Frontend"""
    user = get_user_username(username = payload.username)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect Username or Password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User_Schema_DDBB = Depends(get_current_user)):
    return UserResponse(id=str(current_user.id), username=current_user.username)
