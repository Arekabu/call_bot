from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main import get_main_keyboard
from services.registration import RegistrationService

router = Router()
registration_service = RegistrationService()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Помощь по командам...")


@router.message(F.text == "📝 Регистрация")
async def cmd_register_button(message: Message, state: FSMContext):
    """Обработка нажатия кнопки регистрации"""
    await registration_service.start_registration(message, state)
