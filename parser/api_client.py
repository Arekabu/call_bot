import logging
from http import HTTPStatus
from typing import Any, Dict

import aiohttp

from config import config
from config.dto import TimeUpdateDTO
from exceptions import BaseServiceException, NetworkError, Server500

logger = logging.getLogger(__name__)


class DjangoAPIClient:
    def __init__(self) -> None:
        self.base_url = config.DJANGO_API_URL
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
        telegram_id: str = None,
    ) -> Dict[str, Any]:
        """Базовый метод для HTTP запросов"""
        url = f"{self.base_url}/{endpoint}"
        headers = {}

        if telegram_id:
            headers["Telegram-Id"] = telegram_id

        try:
            async with aiohttp.ClientSession(
                timeout=self.timeout, headers=headers
            ) as session:
                async with session.request(method, url, json=data) as response:
                    response_data = await response.json()
                    detail = response_data.get("detail", None)

                    if response.status in (HTTPStatus.OK, HTTPStatus.CREATED):
                        return response_data
                    elif response.status >= HTTPStatus.INTERNAL_SERVER_ERROR:
                        raise Server500(detail)
                    else:
                        raise BaseServiceException(detail)

        except aiohttp.ClientError as e:
            logger.error(f"Network error: {e}")
            raise NetworkError(f"Network error: {str(e)}")

    async def send_email(self, email: str, telegram_id: str) -> Dict[str, Any]:
        """Регистрация пользователя. Отправка email на сервер."""
        data = {"email": email}
        return await self._make_request("POST", "users/email/", data, telegram_id)

    async def send_code(self, code: str, telegram_id: str) -> Dict[str, Any]:
        """Регистрация пользователя. Отправка code на сервер."""
        data = {"code": code}
        return await self._make_request("POST", "users/code/", data, telegram_id)

    async def get_meetings(self, *, chat_id: str, telegram_id: str) -> Dict[str, Any]:
        """Запрос созвонов. Запросить созвоны пользователя."""
        data = {"chat_id": chat_id}
        return await self._make_request(
            "GET", "meetings/", data, telegram_id=telegram_id
        )

    async def send_time(self, *, time_data: TimeUpdateDTO) -> Dict[str, Any]:
        """Отправка времени обновления данных о созвонах"""
        data = {"time": time_data.time, "chat_id": time_data.chat_id}
        return await self._make_request(
            "POST", "users/set_time/", data, telegram_id=time_data.telegram_id
        )
