from typing import Any, final

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from exceptions import BaseServiceException, TelegramFormatError
from keyboards import get_calls_inline_keyboard
from services.base import BaseService


@final
class MeetingsService(BaseService):
    async def _get_telegram_id(self, **kwargs: Any) -> str:
        callback: CallbackQuery = kwargs["callback"]
        return str(callback.from_user.id)

    async def _call_api(self, telegram_id: str, **kwargs: Any) -> None:
        callback: CallbackQuery = kwargs["callback"]
        chat_id = str(callback.message.chat.id)

        try:
            # Отправляем запрос на сервер
            response_data = await self.api.get_meetings(
                chat_id=chat_id, telegram_id=telegram_id
            )

            # Форматируем ответ
            formatted_text = await self._format_meetings_response(response_data)

            try:
                await callback.message.answer(
                    formatted_text,
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                    reply_markup=get_calls_inline_keyboard(),
                )
            except TelegramBadRequest:
                raise TelegramFormatError

        except BaseServiceException as e:
            # Отправляем полный текст ошибки от сервера
            await callback.message.answer(e.send)

    async def _format_meetings_response(self, response_data: dict) -> str:
        """Форматируем ответа сервера для отправки пользователю"""
        meetings = response_data.get("meetings", [])

        if not meetings:
            return "📭 На сегодня созвонов нет"

        text = "📅 <b>Ваши созвоны на сегодня:</b>\n\n"

        for i, meeting in enumerate(meetings, 1):
            title = (
                meeting["title"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )

            url = meeting["url"]

            text += f"<b>{i}. {title}</b>\n"
            text += f"   🕐 {meeting['meeting_time']}\n"

            if url:
                url = meeting["url"].strip().rstrip('\\"')
                text += f"   🔗 <a href='{url}'>Ссылка</a>\n\n"
            else:
                text += "   🔗 Ссылка не предоставлена.\n\n"

        return text
