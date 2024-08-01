import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger


load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
bot.echoed = False

dp = Dispatcher(storage=MemoryStorage())

scheduler = AsyncIOScheduler()

logger.add("test_bot.log",
           format="{time} {level} {message}",
           rotation="10 MB",
           compression='zip',
           level="INFO")


