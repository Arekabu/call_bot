from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.main import get_main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Помощь по командам...")
