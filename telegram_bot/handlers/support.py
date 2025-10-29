"""Support and feedback handlers"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
import random
import string

from states import SupportStates
from services import api_client
from config import settings

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text.in_(["💬 Підтримка", "💬 Support", "💬 Поддержка", "/support"]))
async def cmd_support(message: Message, state: FSMContext, user: dict):
    """Start support conversation"""
    language = user.get("language", "uk")

    texts = {
        "uk": "💬 Підтримка\n\nОпишіть вашу проблему або питання.\nМенеджер відповість вам найближчим часом.",
        "en": "💬 Support\n\nDescribe your issue or question.\nManager will respond to you soon.",
        "ru": "💬 Поддержка\n\nОпишите вашу проблему или вопрос.\nМенеджер ответит вам в ближайшее время."
    }

    await state.set_state(SupportStates.waiting_for_message)
    await message.answer(texts.get(language, texts["uk"]))


@router.message(SupportStates.waiting_for_message, F.text)
async def process_support_message(message: Message, state: FSMContext, user: dict):
    """Handle support message"""
    language = user.get("language", "uk")
    ticket_id = "SUP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Save to database
    result = await api_client.create_support_message(
        user_id=user["id"],
        telegram_id=message.from_user.id,
        ticket_id=ticket_id,
        message_text=message.text,
        sender_type="user"
    )

    if result:
        # Send to manager channel
        manager_text = f"💬 Нове повідомлення підтримки\n\n"
        manager_text += f"👤 Користувач: {user['full_name']}\n"
        manager_text += f"🆔 Ticket: {ticket_id}\n"
        manager_text += f"📞 Телефон: {user['phone']}\n\n"
        manager_text += f"Повідомлення:\n{message.text}"

        try:
            await message.bot.send_message(settings.MANAGER_CHANNEL_ID, manager_text)
        except Exception as e:
            logger.error(f"Failed to send to manager: {e}")

        texts = {
            "uk": f"✅ Ваше повідомлення надіслано!\n\nНомер звернення: {ticket_id}\n\nМенеджер відповість найближчим часом.",
            "en": f"✅ Your message has been sent!\n\nTicket number: {ticket_id}\n\nManager will respond soon.",
            "ru": f"✅ Ваше сообщение отправлено!\n\nНомер обращения: {ticket_id}\n\nМенеджер ответит в ближайшее время."
        }
        await message.answer(texts.get(language, texts["uk"]))
    else:
        texts = {
            "uk": "❌ Помилка відправки. Спробуйте ще раз.",
            "en": "❌ Send error. Please try again.",
            "ru": "❌ Ошибка отправки. Попробуйте ещё раз."
        }
        await message.answer(texts.get(language, texts["uk"]))

    await state.clear()
