from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards import MainKeyboardCallback
from services import MeetingsService

router = Router()
meetings_service = MeetingsService()


@router.callback_query(F.data == MainKeyboardCallback.MY_CALLS)
async def meetings_button(callback: CallbackQuery):
    """Обработка нажатия кнопки Мои созвоны"""
    await callback.answer()
    await meetings_service(callback=callback)
