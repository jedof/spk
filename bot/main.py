import logging
import asyncio
import os


from aiogram import Bot, Dispatcher
from hendlers import router as hendlers_router
from db.initdb import initdb
from config import settings


logging.basicConfig(level=logging.INFO)


bot = Bot(token=settings.TG_TOKEN.get_secret_value())

    

async def main():
    dp = Dispatcher()
    dp.include_router(hendlers_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await initdb()
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())    
