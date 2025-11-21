from aiogram import F, Router
from aiogram.types import Message

from services.meetings import MeetingsService

router = Router()
meetings_service = MeetingsService()


@router.message(F.text == "📅 Мои созвоны")
async def meetings_button(message: Message):
    """Обработка нажатия кнопки Мои созвоны"""
    await meetings_service.get_meetings(message)
