from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app.keyboards import main
from app.database import get_user_list
from app.weather_api import get_city_weather


router = Router()


class EchoMode:
    def __init__(self):
        self.value = False


echo_mode = EchoMode()


@router.message(CommandStart())
async def start_command(message: Message):
    print(f'hello: {message.from_user.full_name}')
    await message.answer("Добро пожаловать в наш бот!", reply_markup=main)


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Доступные команды: /start, /help, /echo, /photo")


@router.message(Command("echo"))
async def echo_command(message: Message):
    if echo_mode.value:
        echo_mode.value = False
        await message.answer('Режим "эхо" выключен, для отключения еще раз вызовите команду')
    else:
        echo_mode.value = True
        await message.answer('Режим "эхо" включен')


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
    city_name = message.text.replace('/weather ', '')
    city_weather = await get_city_weather(city_name)
    await message.answer(str(city_weather))


