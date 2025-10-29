"""
Authentication middleware to check user registration
"""

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Dict, Any, Awaitable
import logging

from services.api_client import api_client

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseMiddleware):
    """
    Middleware to check if user is registered
    If not registered, redirects to registration flow
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Check user authentication
        """
        telegram_id = None

        # Extract telegram_id
        if isinstance(event, Message):
            telegram_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            telegram_id = event.from_user.id

        if not telegram_id:
            return await handler(event, data)

        # Skip auth check for /start command (registration)
        if isinstance(event, Message) and event.text and event.text.startswith("/start"):
            return await handler(event, data)

        # Check if user exists in database
        try:
            user = await api_client.get_user(telegram_id)

            if user:
                # User exists, add to data
                data["user"] = user
                data["language"] = user.get("language", "uk")
                return await handler(event, data)
            else:
                # User not registered
                if isinstance(event, Message):
                    await event.answer(
                        "❗️ Вам потрібно спочатку зареєструватися.\n"
                        "Натисніть /start для початку реєстрації.\n\n"
                        "❗️ You need to register first.\n"
                        "Press /start to begin registration."
                    )
                elif isinstance(event, CallbackQuery):
                    await event.answer(
                        "Спочатку зареєструйтесь через /start",
                        show_alert=True
                    )
                return  # Stop processing

        except Exception as e:
            logger.error(f"Auth check error: {e}")
            # Continue processing even on error
            return await handler(event, data)
