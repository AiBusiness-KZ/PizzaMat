"""
n8n webhook client for triggering workflows
"""

import httpx
import logging
from typing import Optional, Dict, Any

from config import settings

logger = logging.getLogger(__name__)


class N8NClient:
    """Client for triggering n8n workflows"""

    def __init__(self):
        self.base_url = settings.N8N_URL
        self.webhook_secret = settings.N8N_WEBHOOK_SECRET

    async def _trigger_webhook(
        self,
        webhook_path: str,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Trigger n8n webhook"""
        if not self.base_url:
            logger.warning("N8N_URL not configured, skipping webhook trigger")
            return None

        url = f"{self.base_url}{webhook_path}"

        # Add secret to headers if configured
        headers = {}
        if self.webhook_secret:
            headers["X-Webhook-Secret"] = self.webhook_secret

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    url=url,
                    json=data,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"n8n webhook error {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"n8n webhook request error: {e}")
            return None

    async def validate_receipt(
        self,
        order_id: int,
        receipt_image_url: str,
        expected_amount: float,
        order_code: str
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger receipt validation workflow
        n8n will use GPT-4o Vision to validate the receipt
        """
        data = {
            "order_id": order_id,
            "receipt_image_url": receipt_image_url,
            "expected_amount": expected_amount,
            "order_code": order_code,
            "trigger_source": "telegram_bot"
        }

        return await self._trigger_webhook("/webhook/validate-receipt", data)

    async def notify_manager(
        self,
        order_id: int,
        order_code: str,
        user_name: str,
        total_amount: float,
        location_name: str,
        items: list,
        receipt_validated: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger manager notification workflow
        Sends formatted message to manager channel
        """
        data = {
            "order_id": order_id,
            "order_code": order_code,
            "user_name": user_name,
            "total_amount": total_amount,
            "location_name": location_name,
            "items": items,
            "receipt_validated": receipt_validated,
            "trigger_source": "telegram_bot"
        }

        return await self._trigger_webhook("/webhook/notify-manager", data)

    async def send_analytics_event(
        self,
        event_type: str,
        user_id: int,
        telegram_id: int,
        meta_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Send analytics event to n8n for processing/storage
        """
        data = {
            "event_type": event_type,
            "user_id": user_id,
            "telegram_id": telegram_id,
            "meta_data": meta_data or {},
            "trigger_source": "telegram_bot"
        }

        return await self._trigger_webhook("/webhook/analytics-event", data)


# Global n8n client instance
n8n_client = N8NClient()
