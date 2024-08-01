import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from app.handlers import commands, inlines, forms, texts
from app.database import db_start, get_user_list

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
bot.echoed = False

dp = Dispatcher(storage=MemoryStorage())


async def send_daily_notification():
    user_list = await get_user_list()
    for user in user_list:
        await bot.send_message(user['id'], "Не забудьте проверить уведомления!")


async def on_startup(dispatcher: Dispatcher):
    await db_start()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_notification, 'cron', hour=9, minute=0, timezone='Europe/Moscow')
    scheduler.start()


async def main():
    dp.include_router(commands.router)
    dp.include_router(inlines.router)
    dp.include_router(forms.router)
    dp.include_router(texts.router)

    dp.startup.register(on_startup)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())