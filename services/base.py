from abc import ABC, abstractmethod
from parser.api_client import DjangoAPIClient
from typing import Any, final


class BaseService(ABC):
    def __init__(self) -> None:
        self.api = DjangoAPIClient()

    @final
    async def execute(self, *args: Any, **kwargs: Any) -> None:
        telegram_id = await self._get_telegram_id(*args, **kwargs)
        await self._call_api(telegram_id, *args, **kwargs)

    @abstractmethod
    async def _get_telegram_id(self, *args: Any, **kwargs: Any) -> str:
        pass

    @abstractmethod
    async def _call_api(self, *args: Any, **kwargs: Any) -> None:
        pass
