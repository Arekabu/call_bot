from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard():
    """Главная клавиатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Мои созвоны")],
            [KeyboardButton(text="📝 Регистрация"), KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
    )
