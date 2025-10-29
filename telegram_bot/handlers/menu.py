"""Menu and ordering handlers"""

from aiogram import Router, F
from aiogram.types import Message
import logging

from keyboards import get_webapp_keyboard
from config import settings

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text.in_(["🍕 Меню", "🍕 Menu", "🍕 Меню", "/menu"]))
async def cmd_menu(message: Message, user: dict):
    """Open WebApp menu"""
    language = user.get("language", "uk")
    telegram_id = message.from_user.id

    texts = {
        "uk": "🍕 Виберіть піцу з нашого меню:\n\nНатисніть кнопку нижче, щоб відкрити каталог.",
        "en": "🍕 Choose pizza from our menu:\n\nClick the button below to open catalog.",
        "ru": "🍕 Выберите пиццу из нашего меню:\n\nНажмите кнопку ниже, чтобы открыть каталог."
    }

    webapp_url = f"{settings.WEBAPP_URL}?telegram_id={telegram_id}"

    await message.answer(
        texts.get(language, texts["uk"]),
        reply_markup=get_webapp_keyboard(webapp_url, language)
    )
