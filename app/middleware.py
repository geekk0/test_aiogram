from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag


class ReminderMiddleware(BaseMiddleware):
    def __init__(self, scheduler, user_reminders):
        self.scheduler = scheduler
        self.user_reminders = user_reminders
        super().__init__()

    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            chat_id = event.chat.id
            if get_flag(event, 'reminder'):
                if chat_id in self.user_reminders:
                    self.user_reminders[chat_id].remove()
                    self.user_reminders.pop(chat_id, None)
                    await event.answer("Спасибо за ответ!")
        return await handler(event, data)