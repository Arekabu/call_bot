from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.commands import RegistrationStates
from keyboards.main import get_main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Помощь по командам...")


@router.message(F.text == "📝 Регистрация")
async def cmd_register_button(message: Message, state: FSMContext):
    """Обработка нажатия кнопки регистрации"""
    await message.answer("Введите адрес электронной почты пользователя.")
    await state.set_state(RegistrationStates.waiting_for_email)
