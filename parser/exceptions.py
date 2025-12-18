from typing import final

DEFAULT_API_400_MESSAGE = "❌ Произошла ошибка. Попробуйте еще раз."
DEFAULT_API_500_MESSAGE = "🔥 Внутренняя ошибка сервера. Попробуйте позже."


class BaseServiceException(Exception):
    default_send = DEFAULT_API_400_MESSAGE

    def __init__(self, send: str = None) -> None:
        self.send = send or self.default_send


@final
class Server500(BaseServiceException):
    default_send = DEFAULT_API_500_MESSAGE


@final
class NetworkError(BaseServiceException):
    default_send = "📡 Ошибка сети. Проверьте соединение."


@final
class TelegramFormatError(BaseServiceException):
    default_send = "⚠️ Ошибка при форматировании ответа сервера."
