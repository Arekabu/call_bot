import re
from typing import final

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import MeetingsDTO, MeetingsUpdateTimeStates, UpdateTimeDTO
from exceptions import BaseServiceException, Server500, TelegramFormatError
from keyboards import get_calls_inline_keyboard, get_calls_inline_keyboard_group
from services.base import BaseService


@final
class MeetingsService(BaseService):
    async def _get_telegram_id(self, callback: CallbackQuery) -> str:
        return str(callback.from_user.id)

    async def _call_api(self, telegram_id: str, callback: CallbackQuery) -> None:
        chat_id = str(callback.message.chat.id)

        if chat_id == telegram_id:
            keyboard = get_calls_inline_keyboard()
        else:
            keyboard = get_calls_inline_keyboard_group()

        meetings_data = MeetingsDTO(chat_id=chat_id, telegram_id=telegram_id)

        try:
            # Отправляем запрос на сервер
            response_data = await self.api.get_meetings(meetings_data)

            # Форматируем ответ
            formatted_text = await self._format_meetings_response(response_data)

            try:
                await callback.message.answer(
                    formatted_text,
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                    reply_markup=keyboard,
                )
            except TelegramBadRequest:
                raise TelegramFormatError

        except BaseServiceException as e:
            # Отправляем полный текст ошибки от сервера
            await callback.message.answer(e.send)

    async def _format_meetings_response(self, response_data: dict) -> str:
        """Форматирует ответа сервера"""
        meetings = response_data.get("meetings", [])

        if not meetings:
            return "📭 На сегодня созвонов нет"

        simple_meetings_keys = ["meeting_time", "title", "url"]
        group_meetings_keys = ["username", "events"]

        if isinstance(meetings[0], dict):
            first_meeting = meetings[0]

            if all(key in first_meeting for key in simple_meetings_keys):
                return await self._format_simple_meetings(meetings)

            elif all(key in first_meeting for key in group_meetings_keys):
                return await self._format_group_meetings(meetings)

        return "❌ Неизвестный формат данных"

    async def _format_simple_meetings(self, meetings: list) -> str:
        """Формат ответа для индивидуальных чатов"""

        text = "📅 <b>Ваши созвоны на сегодня:</b>\n\n"

        for i, meeting in enumerate(meetings, 1):
            title = self._escape_html(meeting["title"])

            url = meeting["url"]

            text += f"<b>{i}. {title}</b>\n"
            text += f"   🕐 {meeting['meeting_time']}\n"

            if url:
                url = meeting["url"].strip().rstrip('\\"')
                text += f"   🔗 <a href='{url}'>Ссылка</a>\n\n"
            else:
                text += "   🔗 Ссылка не предоставлена.\n\n"

        return text

    async def _format_group_meetings(self, meetings: list) -> str:
        """Формат ответа для общего чата"""

        text = "📅 <b>Cозвоны на сегодня:</b>\n\n"

        users_with_events = []
        for user_data in meetings:
            if user_data.get("events"):
                users_with_events.append(user_data)

        for n, user_data in enumerate(users_with_events, 1):
            username = user_data["username"]
            events = user_data.get("events", [])

            if not events:
                continue

            text += f"         🎧   <b>{username}</b>\n\n"

            for i, event in enumerate(events, 1):
                title = self._escape_html(event["title"])

                url = event["url"]

                text += f"<b>{i}. {title}</b>\n"
                text += f"   🕐 {event['meeting_time']}\n"

                if url:
                    url = event["url"].strip().rstrip('\\"')
                    text += f"   🔗 <a href='{url}'>Ссылка</a>\n"
                else:
                    text += "   🔗 Ссылка не предоставлена.\n"

            if n != len(users_with_events):
                text += "─" * 19 + "\n\n"

        return text

    def _escape_html(self, text: str) -> str:
        """Экранирование HTML-символов"""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )


@final
class MeetingsUpdateTimeStartService(BaseService):
    async def _get_telegram_id(self, callback: CallbackQuery, state: FSMContext) -> str:
        return str(callback.from_user.id)

    async def _call_api(
        self, telegram_id: str, callback: CallbackQuery, state: FSMContext
    ) -> None:
        await callback.message.answer(
            "Введите желаемое время обновления в формате 00:00"
        )
        await state.set_state(MeetingsUpdateTimeStates.waiting_for_time)


@final
class MeetingsUpdateTimeSendTimeService(BaseService):
    async def _get_telegram_id(self, message: Message, state: FSMContext) -> str:
        return str(message.from_user.id)

    async def _call_api(
        self, telegram_id: str, message: Message, state: FSMContext
    ) -> None:
        """Отправка введённого time на сервер"""
        time = message.text.strip()
        chat_id = str(message.chat.id)

        if not await self._time_is_valid(time):
            await message.answer("Введите время в формате 00:00")
            return None

        time_data = UpdateTimeDTO(time=time, chat_id=chat_id, telegram_id=telegram_id)

        try:
            # Отправляем запрос на сервер
            response_data = await self.api.send_time(time_data=time_data)

            await message.answer(
                response_data.get(
                    "confirm", f"✅ Созвоны будут обновляться по будням в 🕐{time} "
                )
            )
            await state.clear()

        except Server500 as e:
            await message.answer(e.send)
            await state.clear()

            # Для других ошибок оставляем state для возможности повторного ввода
        except BaseServiceException as e:
            await message.answer(e.send)

    async def _time_is_valid(self, time: str) -> bool:
        pattern = re.compile(r"^([0-9]|0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$")
        return bool(re.match(pattern, time))
