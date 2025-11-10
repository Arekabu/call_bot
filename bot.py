import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import config
from handlers.meetings import router as meetings_router
from handlers.start import router as start_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(meetings_router)

    logging.info("Bot starting...")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Bot crashed: {e}")
    finally:
        await bot.session.close()
        logging.info("Bot stopping...")


if __name__ == "__main__":
    asyncio.run(main())
