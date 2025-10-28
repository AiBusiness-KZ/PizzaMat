"""
Dependencies for route handlers
Authentication and authorization
"""

from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from jose import JWTError

from app.core.security import verify_token
from app.config import settings


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Verify JWT token and return current user
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        User data from token
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Parse Bearer token
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    
    try:
        payload = verify_token(token)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Verify that current user is admin
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        Admin user data
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return current_user


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> bool:
    """
    Simple API key verification for internal services
    
    Args:
        x_api_key: API key from header
        
    Returns:
        True if API key is valid
        
    Raises:
        HTTPException: If API key is invalid
    """
    # Get API key from settings
    valid_api_key = settings.JWT_SECRET  # In production use separate API_KEY
    
    if not x_api_key or x_api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    return True
