from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Выбор 1", callback_data="Выбор 1")],
    [InlineKeyboardButton(text="Выбор 2", callback_data="Выбор 2")]
])

# main.add(KeyboardButton("Помощь"), KeyboardButton("Сменить город"))