import logging
from http import HTTPStatus
from parser.exceptions import BaseServiceException, NetworkError, Server500
from typing import Any, Dict

import aiohttp

from config.config import config

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
        return await self._make_request("POST", "users/email", data, telegram_id)

    async def send_code(self, code: str, telegram_id: str) -> Dict[str, Any]:
        """Регистрация пользователя. Отправка code на сервер."""
        data = {"code": code}
        return await self._make_request("POST", "users/code", data, telegram_id)

    async def get_meetings(self, telegram_id: str) -> Dict[str, Any]:
        """Запрос созвонов. Запросить созвоны пользователя."""
        return await self._make_request("GET", "meetings", telegram_id=telegram_id)
