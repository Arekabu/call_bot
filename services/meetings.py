from parser.api_client import DjangoAPIClient
from parser.exceptions import BaseServiceException

from aiogram.types import Message


class MeetingsService:
    def __init__(self) -> None:
        self.api_client = DjangoAPIClient()

    async def get_meetings(self, message: Message) -> None:
        """Запрос созвонов пользователя"""
        telegram_id = str(message.from_user.id)

        try:
            # Отправляем запрос на сервер
            response_data = await self.api_client.get_meetings(telegram_id)

            # Форматируем ответ
            formatted_text = await self._format_meetings_response(response_data)

            await message.answer(
                formatted_text, parse_mode="Markdown", disable_web_page_preview=True
            )

        except BaseServiceException as e:
            # Отправляем полный текст ошибки от сервера
            await message.answer(e.send)

    async def _format_meetings_response(self, response_data: dict) -> str:
        """Форматируем ответа сервера для отправки пользователю"""
        meetings = response_data.get("meetings", [])

        if not meetings:
            return "📭 На сегодня созвонов нет"

        text = "📅 *Ваши созвоны на сегодня:*\n\n"

        for i, meeting in enumerate(meetings, 1):
            time_range = f"{meeting["date_from"][-5:]}  -  {meeting["date_till"][-5:]}"

            text += f"*{i}. {meeting['title']}*\n"
            text += f"   🕐 {time_range}\n"
            text += f"   🔗 [Ссылка]({meeting['url']})\n\n"

        return text
