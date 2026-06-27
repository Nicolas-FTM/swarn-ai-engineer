from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from typing import Optional
from shared.config import settings
from shared.schemas.user import User_Schema_DDBB
from shared.utils.postgres import get
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Logger
import logging
logger = logging.getLogger(__name__)

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/frontend/login")

#####################
# (Un)Hash passwords
#####################
def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode("utf-8"),
    )


#####################
# (De)Code jwt tokens
#####################
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT access token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

#####################
# Authenticate User
#####################
def authenticate_user(username: str, password: str) -> Optional[User_Schema_DDBB]:
    """Authenticate a user by username and password."""
    user = get(
        model=User_Schema_DDBB,
        filters={"username": username}
        )
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

##############################
# Get User from the JWT Token
##############################
def get_current_user(token: str = Depends(oauth2_scheme)) -> User_Schema_DDBB:
    """Get the current authenticated user from the JWT token."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    payload = decode_access_token(token)
    
    id: str = payload.get("sub", None)
   
    if id is None:
        raise credentials_exception
    
    user = get(
        model=User_Schema_DDBB,
        filters={"id": id}
        )
    
    if user is None:
        raise credentials_exception
    
    return user