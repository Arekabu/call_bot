from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.states import RegistrationStates
from services import (
    RegistrationCodeService,
    RegistrationEmailService,
    RegistrationStartService,
)

router = Router()
registration_code_service = RegistrationCodeService()
registration_email_service = RegistrationEmailService()
registration_start_service = RegistrationStartService()


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    """Команда начала процесса регистрации"""
    await registration_start_service.execute(message, state)


@router.message(RegistrationStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    """Обработка введенного email"""
    await registration_email_service.execute(message, state)


@router.message(RegistrationStates.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    """Обработка введенного кода"""
    await registration_code_service.execute(message, state)
