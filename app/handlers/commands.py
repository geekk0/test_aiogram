from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import datetime, timedelta

from app.keyboards import main
from app.database import get_user_list
from app.middleware import ReminderMiddleware
from app.weather_api import get_city_weather
from app.bot_setup import bot, scheduler, logger


router = Router()


class EchoMode:
    def __init__(self):
        self.value = False


echo_mode = EchoMode()

user_reminders = {}


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Добро пожаловать в наш бот!", reply_markup=main)


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Доступные команды: /start, /help, /echo, /photo /users /register /weather /reminder")


@router.message(Command("echo"))
async def echo_command(message: Message):
    if echo_mode.value:
        echo_mode.value = False
        await message.answer('Режим "эхо" выключен')
    else:
        echo_mode.value = True
        await message.answer('Режим "эхо" включен, для отключения еще раз вызовите команду')


@router.message(Command("users"))
async def show_users_list(message: Message):
    users = await get_user_list()
    if users:
        user_list = "\n".join([f"Имя: {user['name']}, Возраст: {user['age']} лет, ID: {user['id']}" for user in users])
        await message.answer(str(user_list))
    else:
        await message.answer("Пользователей пока не зарегистрировано")


@router.message(Command("weather"))
async def show_weather(message: Message):
    try:
        city_name = message.text.replace('/weather ', '')
        city_weather = await get_city_weather(city_name)
        await message.answer(str(city_weather))
    except Exception as e:
        await message.answer("Произошла ошибка, попробуйте позже")
        logger.error(e)


@router.message(Command("reminder"))
async def init_reminder(message: Message):
    job = scheduler.add_job(send_reminder, 'date', run_date=datetime.now() + timedelta(minutes=15),
                            args=[message.from_user.id])
    user_reminders[message.from_user.id] = job

    await message.answer(f"Привет, {message.from_user.first_name}! Как ты сегодня?")


@router.message()
async def handle_message(message: Message):
    chat_id = message.chat.id

    if echo_mode.value:
        await message.answer(message.text)

    if chat_id in user_reminders:
        user_reminders[chat_id].remove()
        user_reminders.pop(chat_id, None)
        await message.answer("Спасибо за ответ!")


async def send_reminder(user_id):
    user_reminders.pop(user_id, None)
    await bot.send_message(user_id, "Вы забыли ответить")


router.message.middleware(ReminderMiddleware(scheduler, user_reminders))



