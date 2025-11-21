from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.states import RegistrationStates
from services.registration import RegistrationService

router = Router()
registration_service = RegistrationService()


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    """Команда начала процесса регистрации"""
    await registration_service.start_registration(message, state)


@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    """Обработка введенного email"""
    await registration_service.process_email(message, state)


@router.message(RegistrationStates.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    """Обработка введенного кода"""
    await registration_service.process_code(message, state)
