from aiogram import Router, F
from aiogram.types import Message

from app.handlers.commands import echo_mode

router = Router()


@router.message(F.text)
async def check_echo(message: Message):
    if not echo_mode:
        return
    await message.answer(message.text)
