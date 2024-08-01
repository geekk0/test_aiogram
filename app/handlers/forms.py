from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ChatPhoto
from aiogram.filters import Command

from app.database import save_user
from app.bot_setup import logger

router = Router()


class RegForm(StatesGroup):
    name = State()
    age = State()


class PhotoState(StatesGroup):
    waiting_for_photo = State()


@router.message(Command("register"))
async def start_questions(message: Message, state: FSMContext):
    await state.set_state(RegForm.name)
    await message.answer(
        "Укажите Ваше имя",
    )


@router.message(RegForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegForm.age)
    await message.answer(
        "Укажите Ваш возраст",
    )


@router.message(RegForm.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    data = await state.get_data()
    msg_text = (f'Спасибо, регистрация завершена. \n '
                f'Ваше имя: {data.get("name")}\n '
                f'Ваш возраст: {data.get("age")}')
    await message.answer(msg_text)
    await save_user(message.from_user.id, data.get("name"), data.get("age"))
    await state.clear()


@router.message(Command("photo"))
async def photo_command(message: Message, state: FSMContext):
    await state.set_state(PhotoState.waiting_for_photo)
    await message.answer("Отправьте фото пожалуйста.")


@router.message(PhotoState.waiting_for_photo)
async def handle_photo(message: Message, state: FSMContext):
    print(message)
    if message.photo:
        largest_photo = message.photo[-1]
        await message.answer(f"Спасибо, фото получено\n "
                             f"Ширина: {largest_photo.width} пикселей \n "
                             f"Высота: {largest_photo.height} пикселей")
    else:
        await message.answer("Произошла ошибка, попробуйте позже")
        logger.error(f"Invalid file type")
    await state.clear()
