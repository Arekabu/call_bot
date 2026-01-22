from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from keyboards import MainKeyboardCallback


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Мои созвоны")],
            [KeyboardButton(text="📝 Регистрация"), KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
    )


def get_main_inline_keyboard() -> InlineKeyboardMarkup:
    """Главная inline-клавиатура"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Мои созвоны", callback_data=MainKeyboardCallback.MY_CALLS
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Регистрация", callback_data=MainKeyboardCallback.REGISTER
                ),
                InlineKeyboardButton(
                    text="❓ Помощь", callback_data=MainKeyboardCallback.HELP
                ),
            ],
        ]
    )


def get_calls_inline_keyboard() -> InlineKeyboardMarkup:
    """inline-клавиатура с кнопкой Мои созвоны"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Обновить", callback_data=MainKeyboardCallback.MY_CALLS
                )
            ],
            [
                InlineKeyboardButton(
                    text="🕐 Установить время",
                    callback_data=MainKeyboardCallback.UPDATE_TIME,
                )
            ],
        ]
    )


def get_calls_inline_keyboard_group() -> InlineKeyboardMarkup:
    """inline-клавиатура с кнопкой Мои созвоны"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Обновить", callback_data=MainKeyboardCallback.MY_CALLS
                )
            ],
        ]
    )
