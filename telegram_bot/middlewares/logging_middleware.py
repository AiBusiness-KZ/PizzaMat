"""
Logging middleware to track all bot interactions
This is KEY for manager analytics and dialog tracking
"""

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Dict, Any, Awaitable
import logging
from datetime import datetime

from services.api_client import api_client

logger = logging.getLogger(__name__)


class InteractionLoggingMiddleware(BaseMiddleware):
    """
    Middleware to log all user interactions to database
    Tracks: commands, messages, callback queries, etc.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Process every update and log it
        """
        telegram_id = None
        user_id = None
        interaction_type = None
        command = None
        message_text = None
        callback_data = None
        chat_id = None
        message_id = None
        fsm_state = None

        # Get FSM state if available
        state = data.get("state")
        if state:
            current_state = await state.get_state()
            fsm_state = current_state

        # Determine interaction type and extract data
        if isinstance(event, Message):
            telegram_id = event.from_user.id
            chat_id = event.chat.id
            message_id = event.message_id

            # Check if it's a command
            if event.text and event.text.startswith("/"):
                interaction_type = "command"
                command = event.text.split()[0]
            elif event.photo:
                interaction_type = "photo"
                message_text = event.caption
            elif event.document:
                interaction_type = "document"
                message_text = event.caption
            elif event.contact:
                interaction_type = "contact"
                message_text = f"Phone: {event.contact.phone_number}"
            else:
                interaction_type = "message"
                message_text = event.text

        elif isinstance(event, CallbackQuery):
            telegram_id = event.from_user.id
            chat_id = event.message.chat.id if event.message else None
            message_id = event.message.message_id if event.message else None
            interaction_type = "callback_query"
            callback_data = event.data

        # Get user_id from data if available (set by auth middleware)
        user_data = data.get("user")
        if user_data:
            user_id = user_data.get("id")

        # Store interaction info for later (after handler execution)
        interaction_data = {
            "telegram_id": telegram_id,
            "user_id": user_id,
            "interaction_type": interaction_type,
            "command": command,
            "message_text": message_text,
            "callback_data": callback_data,
            "chat_id": chat_id,
            "message_id": message_id,
            "fsm_state": fsm_state,
            "timestamp": datetime.utcnow()
        }

        # Call the handler
        bot_response = None
        bot_response_type = None
        is_successful = True
        error_message = None

        try:
            result = await handler(event, data)
            bot_response = "Handler executed successfully"
            bot_response_type = "success"
            return result

        except Exception as e:
            logger.error(f"Handler error: {e}")
            is_successful = False
            error_message = str(e)
            bot_response_type = "error"
            raise

        finally:
            # Log interaction to database (fire and forget)
            if telegram_id:
                try:
                    await api_client.log_interaction(
                        telegram_id=telegram_id,
                        interaction_type=interaction_type,
                        user_id=user_id,
                        command=command,
                        message_text=message_text,
                        callback_data=callback_data,
                        chat_id=chat_id,
                        message_id=message_id,
                        bot_response=bot_response,
                        bot_response_type=bot_response_type,
                        fsm_state=fsm_state,
                        is_successful=is_successful,
                        error_message=error_message,
                        metadata={
                            "duration_ms": int((datetime.utcnow() - interaction_data["timestamp"]).total_seconds() * 1000)
                        }
                    )
                except Exception as log_error:
                    logger.error(f"Failed to log interaction: {log_error}")


class SessionTrackingMiddleware(BaseMiddleware):
    """
    Middleware to track user sessions
    Creates session on first interaction, updates metrics
    """

    def __init__(self):
        super().__init__()
        self.active_sessions = {}  # telegram_id -> session_id

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Track user session
        """
        telegram_id = None
        user_id = None

        # Extract user info
        if isinstance(event, Message):
            telegram_id = event.from_user.id
            user_info = event.from_user
        elif isinstance(event, CallbackQuery):
            telegram_id = event.from_user.id
            user_info = event.from_user
        else:
            return await handler(event, data)

        # Get user_id from data if available
        user_data = data.get("user")
        if user_data:
            user_id = user_data.get("id")

        # Check if session exists
        session_id = self.active_sessions.get(telegram_id)

        if not session_id and user_id:
            # Create new session
            try:
                session_result = await api_client.log_session_start(
                    user_id=user_id,
                    telegram_id=telegram_id,
                    username=user_info.username,
                    first_name=user_info.first_name,
                    last_name=user_info.last_name,
                    language=user_info.language_code,
                    platform=self._detect_platform(event)
                )
                if session_result:
                    session_id = session_result.get("id")
                    self.active_sessions[telegram_id] = session_id
                    logger.info(f"Created session {session_id} for user {telegram_id}")
            except Exception as e:
                logger.error(f"Failed to create session: {e}")

        # Add session_id to data for interaction logging
        if session_id:
            data["session_id"] = session_id

        # Call handler
        return await handler(event, data)

    def _detect_platform(self, event) -> str:
        """Detect user platform from update"""
        # This is a simplified detection
        # You might want to use user agent or other methods
        return "telegram"
