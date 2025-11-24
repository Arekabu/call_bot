from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.main import get_main_inline_keyboard
from services.registration import RegistrationService

router = Router()
registration_service = RegistrationService()


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = """
📞 *Добро пожаловать!*

Это бот для управления вашими созвонами.
Выберите действие:
    """
    await message.answer(
        text, parse_mode="Markdown", reply_markup=get_main_inline_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработка команды help"""
    await message.answer("Помощь по командам...")


@router.callback_query(F.data == "help")
async def help_button(callback: CallbackQuery):
    """Обработка нажатия кнопки Помощь"""
    await callback.answer()
    await callback.message.answer("Тут будет помощь")


@router.callback_query(F.data == "register")
async def register_button(callback: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки регистрации"""
    await callback.answer()
    await registration_service.start_registration(callback.message, state)
