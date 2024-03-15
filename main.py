import logging
import asyncio
import os


from aiogram import Bot, Dispatcher
from hendlers import router as hendlers_router
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TG_TOKEN")


logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)
    

async def main():
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    dp.include_router(hendlers_router)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())    
