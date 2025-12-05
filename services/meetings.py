from parser.exceptions import BaseServiceException
from typing import final

from aiogram.types import CallbackQuery

from services.base import BaseService


@final
class MeetingsService(BaseService):
    async def _get_telegram_id(self, callback: CallbackQuery) -> str:
        return str(callback.from_user.id)

    async def _call_api(self, telegram_id: str, callback: CallbackQuery) -> None:
        try:
            # Отправляем запрос на сервер
            response_data = await self.api.get_meetings(telegram_id)

            # Форматируем ответ
            formatted_text = await self._format_meetings_response(response_data)

            await callback.message.answer(
                formatted_text, parse_mode="Markdown", disable_web_page_preview=True
            )
        except BaseServiceException as e:
            # Отправляем полный текст ошибки от сервера
            await callback.message.answer(e.send)

    async def _format_meetings_response(self, response_data: dict) -> str:
        """Форматируем ответа сервера для отправки пользователю"""
        meetings = response_data.get("meetings", [])

        if not meetings:
            return "📭 На сегодня созвонов нет"

        text = "📅 *Ваши созвоны на сегодня:*\n\n"

        for i, meeting in enumerate(meetings, 1):
            text += f"*{i}. {meeting['title']}*\n"
            text += f"   🕐 {meeting['meeting_time']}\n"
            text += f"   🔗 [Ссылка]({meeting['url']})\n\n"

        return text
