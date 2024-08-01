from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data.in_(['Выбор 1', 'Выбор 2']))
async def show_choice(callback: CallbackQuery):
    await callback.message.answer(f'Вы выбрали: {callback.data}')
