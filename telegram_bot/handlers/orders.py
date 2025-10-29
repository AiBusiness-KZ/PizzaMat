"""Order management handlers"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from states import OrderStates
from keyboards import get_order_actions_keyboard
from services import api_client, n8n_client
from config import settings

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text.in_(["📦 Мої замовлення", "📦 My Orders", "📦 Мои заказы", "/orders"]))
async def cmd_orders(message: Message, user: dict):
    """Show user orders history"""
    language = user.get("language", "uk")
    telegram_id = message.from_user.id

    orders = await api_client.get_user_orders(telegram_id, limit=10)

    if not orders:
        texts = {
            "uk": "📦 У вас ще немає замовлень.\n\nОформіть ваше перше замовлення через 🍕 Меню",
            "en": "📦 You don't have any orders yet.\n\nPlace your first order via 🍕 Menu",
            "ru": "📦 У вас еще нет заказов.\n\nОформите ваш первый заказ через 🍕 Меню"
        }
        await message.answer(texts.get(language, texts["uk"]))
        return

    texts = {
        "uk": "📦 Ваші замовлення:\n\n",
        "en": "📦 Your orders:\n\n",
        "ru": "📦 Ваши заказы:\n\n"
    }

    text = texts.get(language, texts["uk"])

    for order in orders[:5]:
        status_emoji = {
            "pending": "⏳",
            "paid": "💳",
            "confirmed": "✅",
            "completed": "🎉",
            "cancelled": "❌"
        }
        emoji = status_emoji.get(order["status"], "📦")

        text += f"{emoji} Замовлення #{order['order_code']}\n"
        text += f"   Сума: {order['total_amount']} грн\n"
        text += f"   Статус: {order['status']}\n\n"

    await message.answer(text)


@router.message(OrderStates.waiting_for_receipt, F.photo)
async def process_receipt(message: Message, state: FSMContext):
    """Handle receipt photo upload"""
    data = await state.get_data()
    order_id = data.get("order_id")
    user = data.get("user")
    language = user.get("language", "uk")

    # Download photo
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    photo_bytes = await message.bot.download_file(file.file_path)

    # Upload to backend
    result = await api_client.upload_receipt(order_id, photo_bytes.read())

    if result:
        # Trigger n8n for AI validation
        await n8n_client.validate_receipt(
            order_id=order_id,
            receipt_image_url=result["receipt_image_url"],
            expected_amount=result["total_amount"],
            order_code=result["order_code"]
        )

        texts = {
            "uk": "✅ Чек завантажено!\n\n⏳ Перевіряємо чек за допомогою AI...\n\nВи отримаєте повідомлення після перевірки.",
            "en": "✅ Receipt uploaded!\n\n⏳ Validating receipt using AI...\n\nYou'll receive notification after validation.",
            "ru": "✅ Чек загружен!\n\n⏳ Проверяем чек с помощью AI...\n\nВы получите уведомление после проверки."
        }
        await message.answer(texts.get(language, texts["uk"]))
    else:
        texts = {
            "uk": "❌ Помилка завантаження чека. Спробуйте ще раз.",
            "en": "❌ Receipt upload error. Please try again.",
            "ru": "❌ Ошибка загрузки чека. Попробуйте ещё раз."
        }
        await message.answer(texts.get(language, texts["uk"]))

    await state.clear()
