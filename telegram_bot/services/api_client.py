"""
Backend API client for making requests to FastAPI backend
"""

import httpx
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)


class BackendAPIClient:
    """Client for interacting with FastAPI backend"""

    def __init__(self):
        self.base_url = settings.BACKEND_URL
        self.timeout = settings.BACKEND_TIMEOUT

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make HTTP request to backend"""
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    data=data,
                    json=json_data,
                    files=files
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None

    # ==================== User Endpoints ====================

    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by Telegram ID"""
        return await self._request("GET", f"/api/users/{telegram_id}")

    async def create_user(
        self,
        telegram_id: int,
        phone: str,
        full_name: str,
        city_id: Optional[int] = None,
        language: str = "uk"
    ) -> Optional[Dict[str, Any]]:
        """Create new user"""
        data = {
            "telegram_id": telegram_id,
            "phone": phone,
            "full_name": full_name,
            "language": language
        }
        if city_id:
            data["city_id"] = city_id

        return await self._request("POST", "/api/users", json_data=data)

    async def update_user(
        self,
        telegram_id: int,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Update user"""
        return await self._request("PUT", f"/api/users/{telegram_id}", json_data=kwargs)

    # ==================== Menu Endpoints ====================

    async def get_categories(self) -> Optional[List[Dict[str, Any]]]:
        """Get all active categories"""
        result = await self._request("GET", "/api/categories")
        return result if result else []

    async def get_products(self, category_id: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """Get all active products"""
        endpoint = "/api/products"
        if category_id:
            endpoint += f"?category_id={category_id}"
        result = await self._request("GET", endpoint)
        return result if result else []

    async def get_locations(self, city_id: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
        """Get all active pickup locations"""
        endpoint = "/api/pickup-locations"
        if city_id:
            endpoint += f"?city_id={city_id}"
        result = await self._request("GET", endpoint)
        return result if result else []

    async def get_cities(self) -> Optional[List[Dict[str, Any]]]:
        """Get all active cities"""
        result = await self._request("GET", "/api/cities")
        return result if result else []

    # ==================== Order Endpoints ====================

    async def create_order(
        self,
        user_id: int,
        location_id: int,
        items: List[Dict[str, Any]],
        total_amount: float
    ) -> Optional[Dict[str, Any]]:
        """Create new order"""
        data = {
            "user_id": user_id,
            "location_id": location_id,
            "items": items,
            "total_amount": total_amount
        }
        return await self._request("POST", "/api/orders", json_data=data)

    async def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        """Get order by ID"""
        return await self._request("GET", f"/api/orders/{order_id}")

    async def get_user_orders(
        self,
        telegram_id: int,
        limit: int = 10
    ) -> Optional[List[Dict[str, Any]]]:
        """Get user's orders"""
        result = await self._request("GET", f"/api/orders/user/{telegram_id}?limit={limit}")
        return result if result else []

    async def upload_receipt(
        self,
        order_id: int,
        image_bytes: bytes,
        filename: str = "receipt.jpg"
    ) -> Optional[Dict[str, Any]]:
        """Upload receipt image for order"""
        files = {"file": (filename, image_bytes, "image/jpeg")}
        return await self._request("POST", f"/api/orders/{order_id}/receipt", files=files)

    async def update_order_status(
        self,
        order_id: int,
        status: str,
        cancellation_reason: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update order status"""
        data = {"status": status}
        if cancellation_reason:
            data["cancellation_reason"] = cancellation_reason
        return await self._request("PUT", f"/api/orders/{order_id}/status", json_data=data)

    # ==================== Interaction Logging ====================

    async def log_session_start(
        self,
        user_id: int,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        language: Optional[str] = None,
        platform: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Log session start"""
        data = {
            "user_id": user_id,
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language": language,
            "platform": platform
        }
        return await self._request("POST", "/api/sessions", json_data=data)

    async def log_session_end(self, session_id: int) -> Optional[Dict[str, Any]]:
        """Log session end"""
        return await self._request("PUT", f"/api/sessions/{session_id}/end")

    async def log_interaction(
        self,
        telegram_id: int,
        interaction_type: str,
        session_id: Optional[int] = None,
        user_id: Optional[int] = None,
        command: Optional[str] = None,
        message_text: Optional[str] = None,
        callback_data: Optional[str] = None,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        bot_response: Optional[str] = None,
        bot_response_type: Optional[str] = None,
        fsm_state: Optional[str] = None,
        meta_data: Optional[Dict[str, Any]] = None,
        is_successful: bool = True,
        error_message: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Log bot interaction"""
        data = {
            "telegram_id": telegram_id,
            "interaction_type": interaction_type,
            "session_id": session_id,
            "user_id": user_id,
            "command": command,
            "message_text": message_text,
            "callback_data": callback_data,
            "chat_id": chat_id,
            "message_id": message_id,
            "bot_response": bot_response,
            "bot_response_type": bot_response_type,
            "fsm_state": fsm_state,
            "meta_data": meta_data,
            "is_successful": is_successful,
            "error_message": error_message
        }
        return await self._request("POST", "/api/interactions", json_data=data)

    # ==================== Support Messages ====================

    async def create_support_message(
        self,
        user_id: int,
        telegram_id: int,
        ticket_id: str,
        message_text: str,
        sender_type: str = "user",
        message_type: str = "text",
        file_url: Optional[str] = None,
        order_id: Optional[int] = None,
        thread_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Create support message"""
        data = {
            "user_id": user_id,
            "telegram_id": telegram_id,
            "ticket_id": ticket_id,
            "message_text": message_text,
            "sender_type": sender_type,
            "message_type": message_type,
            "file_url": file_url,
            "order_id": order_id,
            "thread_id": thread_id
        }
        return await self._request("POST", "/api/support", json_data=data)


# Global API client instance
api_client = BackendAPIClient()
