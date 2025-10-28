"""
Rate limiting middleware
Protects API from abuse and DDoS attacks
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException, status
from typing import Callable
import time
from collections import defaultdict
from datetime import datetime, timedelta


# Create limiter instance
limiter = Limiter(key_func=get_remote_address)


# In-memory storage for rate limiting (use Redis in production)
class SimpleRateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if request is allowed based on rate limit
        
        Args:
            key: Identifier for the client (IP, user_id, etc.)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        window_start = now - window_seconds
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        # Check if limit is exceeded
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True
    
    def cleanup_old_entries(self, max_age_seconds: int = 3600):
        """Remove entries older than max_age_seconds"""
        now = time.time()
        keys_to_remove = []
        
        for key, requests in self.requests.items():
            if not requests or max(requests) < now - max_age_seconds:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.requests[key]


# Global rate limiter instance
simple_rate_limiter = SimpleRateLimiter()


def rate_limit_dependency(max_requests: int = 100, window_seconds: int = 60):
    """
    FastAPI dependency for rate limiting
    
    Usage:
        @app.get("/endpoint", dependencies=[Depends(rate_limit_dependency(max_requests=10, window_seconds=60))])
    """
    async def _rate_limit(request: Request):
        client_ip = request.client.host if request.client else "unknown"
        
        if not simple_rate_limiter.is_allowed(client_ip, max_requests, window_seconds):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds.",
                headers={"Retry-After": str(window_seconds)}
            )
        
        return True
    
    return _rate_limit
