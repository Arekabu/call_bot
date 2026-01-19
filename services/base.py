from abc import ABC, abstractmethod
from parser.api_client import DjangoAPIClient
from typing import Any, final


class BaseService(ABC):
    def __init__(self) -> None:
        self.api = DjangoAPIClient()

    @final
    async def __call__(self, **kwargs: Any) -> None:
        telegram_id = await self._get_telegram_id(**kwargs)
        await self._call_api(telegram_id=telegram_id, **kwargs)

    @abstractmethod
    async def _get_telegram_id(self, **kwargs: Any) -> str:
        pass

    @abstractmethod
    async def _call_api(self, telegram_id: str, **kwargs: Any) -> None:
        pass
