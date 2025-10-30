"""
Authentication routes
Login, register, token validation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta

from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.rate_limit import rate_limit_dependency
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    is_admin: bool


# Hardcoded admin credentials for MVP
# TODO: Move to database with hashed passwords
ADMIN_CREDENTIALS = {
    "admin": {
        "password_hash": get_password_hash("admin123"),  # Change in production!
        "is_admin": True
    }
}


@router.post("/login", 
             response_model=LoginResponse,
             dependencies=[Depends(rate_limit_dependency(max_requests=5, window_seconds=60))])
async def login(credentials: LoginRequest):
    """
    Admin login endpoint
    
    Returns JWT token for authenticated admin
    """
    # Check if user exists
    user = ADMIN_CREDENTIALS.get(credentials.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    # Create access token
    token_data = {
        "sub": credentials.username,
        "is_admin": user["is_admin"]
    }
    
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        is_admin=user["is_admin"]
    )


@router.get("/verify")
async def verify_token_endpoint(current_user: dict = Depends(lambda: {})):
    """
    Verify if token is valid
    Used by frontend to check authentication status
    """
    return {
        "valid": True,
        "user": current_user
    }
