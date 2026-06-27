"""
User management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from shared.schemas.user import UserCreate, UserResponse

# Definition of the router
router = APIRouter(
    prefix="/api/frontend",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """
    Register a new user.
    """
    # TODO: Implement user registration
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User registration not yet implemented",
    )


@router.post("/login")
async def login(email: str, password: str):
    """
    Login user and return JWT token.
    """
    # TODO: Implement login
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login not yet implemented",
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """
    Get current authenticated user.
    """
    # TODO: Implement get current user
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Get current user not yet implemented",
    )
