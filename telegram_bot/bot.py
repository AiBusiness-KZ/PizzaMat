"""
PizzaMat Telegram Bot
Main entry point
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from middlewares import AuthMiddleware, InteractionLoggingMiddleware, SessionTrackingMiddleware
from handlers import start, menu, orders, support, manager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function"""

    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Use memory storage for FSM
    # In production, consider using Redis storage
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register middlewares
    # Order matters! Session tracking -> Auth -> Logging
    dp.message.middleware(SessionTrackingMiddleware())
    dp.callback_query.middleware(SessionTrackingMiddleware())

    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    dp.message.middleware(InteractionLoggingMiddleware())
    dp.callback_query.middleware(InteractionLoggingMiddleware())

    # Register routers
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(orders.router)
    dp.include_router(support.router)
    dp.include_router(manager.router)

    logger.info("Bot starting...")
    logger.info(f"Backend URL: {settings.BACKEND_URL}")
    logger.info(f"Manager Channel ID: {settings.MANAGER_CHANNEL_ID}")

    # Start polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
