import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import handler
from ENV.env import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Main bot function"""
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set in environment variables")
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(handler.rt)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
