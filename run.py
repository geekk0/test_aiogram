import asyncio

import app.handlers.commands as commands
import app.handlers.forms as forms
import app.handlers.inlines as inlines
import app.handlers.texts as texts

from app.bot_setup import bot, dp, scheduler, logger
from app.database import db_start, get_user_list


async def send_daily_notification():
    user_list = await get_user_list()
    for user in user_list:
        await bot.send_message(user['id'], "Не забудьте проверить уведомления!")


async def on_startup():
    await db_start()
    scheduler.add_job(send_daily_notification, 'cron', hour=9, minute=0, timezone='Europe/Moscow')
    scheduler.start()


async def main():
    logger.info("Starting bot...")
    dp.include_router(inlines.router)
    dp.include_router(forms.router)
    dp.include_router(commands.router)
    dp.include_router(texts.router)

    dp.startup.register(on_startup)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())