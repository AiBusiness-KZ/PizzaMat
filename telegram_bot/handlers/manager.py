"""Manager callback handlers"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
import logging

from services import api_client

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("manager_confirm_"))
async def manager_confirm_order(callback: CallbackQuery):
    """Manager confirms order"""
    order_id = int(callback.data.split("_")[2])

    result = await api_client.update_order_status(order_id, "confirmed")

    if result:
        await callback.message.edit_text(
            callback.message.text + "\n\n✅ ПІДТВЕРДЖЕНО"
        )

        # Notify user
        order = await api_client.get_order(order_id)
        if order:
            user_text = f"🎉 Ваше замовлення #{order['order_code']} підтверджено!\n\n"
            user_text += f"📍 Адреса для самовивозу:\n{order['location']['address']}\n\n"
            user_text += f"⏰ Час роботи: {order['location']['working_hours']}\n\n"
            user_text += f"Код для отримання: {order['order_code']}"

            try:
                await callback.bot.send_message(order["user"]["telegram_id"], user_text)
            except Exception as e:
                logger.error(f"Failed to notify user: {e}")

        await callback.answer("Замовлення підтверджено!")
    else:
        await callback.answer("Помилка!", show_alert=True)


@router.callback_query(F.data.startswith("manager_reject_"))
async def manager_reject_order(callback: CallbackQuery):
    """Manager rejects order"""
    order_id = int(callback.data.split("_")[2])

    result = await api_client.update_order_status(order_id, "cancelled", "Відхилено менеджером")

    if result:
        await callback.message.edit_text(
            callback.message.text + "\n\n❌ ВІДХИЛЕНО"
        )

        # Notify user
        order = await api_client.get_order(order_id)
        if order:
            user_text = f"❌ Ваше замовлення #{order['order_code']} було відхилено.\n\n"
            user_text += f"Причина: Не пройдено перевірку чека.\n\n"
            user_text += f"Будь ласка, зв'яжіться з підтримкою: /support"

            try:
                await callback.bot.send_message(order["user"]["telegram_id"], user_text)
            except Exception as e:
                logger.error(f"Failed to notify user: {e}")

        await callback.answer("Замовлення відхилено!")
    else:
        await callback.answer("Помилка!", show_alert=True)
