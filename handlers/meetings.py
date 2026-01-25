from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import MeetingsUpdateTimeStates
from keyboards import MainKeyboardCallback
from services import (
    MeetingsService,
    MeetingsUpdateTimeSendTimeService,
    MeetingsUpdateTimeStartService,
)

router = Router()
meetings_service = MeetingsService()
meetings_update_time_start_service = MeetingsUpdateTimeStartService()
meetings_update_time_send_time_service = MeetingsUpdateTimeSendTimeService()


@router.callback_query(F.data == MainKeyboardCallback.MY_CALLS)
async def meetings_button(callback: CallbackQuery):
    """Обработка нажатия кнопки Мои созвоны"""
    await callback.answer()
    await meetings_service(callback=callback)


@router.callback_query(F.data == MainKeyboardCallback.UPDATE_TIME)
async def set_time_button(callback: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки Установить время"""
    await callback.answer()
    await meetings_update_time_start_service(callback=callback, state=state)


@router.message(MeetingsUpdateTimeStates.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    """Обработка введенного времени"""
    await meetings_update_time_send_time_service(message=message, state=state)
