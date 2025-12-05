from parser.api_client import DjangoAPIClient
from unittest.mock import AsyncMock

import pytest
from aiohttp import web


@pytest.fixture
async def api_client():
    return DjangoAPIClient()


@pytest.fixture
def mock_message():
    """Фикстура для сообщения"""
    message = AsyncMock()
    message.from_user.id = 123456
    return message


@pytest.fixture
def mock_callback():
    """Фикстура для коллбэка"""
    callback = AsyncMock()
    callback.from_user.id = 123456
    callback.message.answer = AsyncMock()
    return callback


@pytest.fixture
async def test_server_factory(aiohttp_server):
    """Фабрика возвращает настроенный клиент"""

    async def factory(handler, path="/api/test", methods=None):
        # Импортируем локально, чтобы при каждом вызове создавался уникальный клиент
        from parser.api_client import DjangoAPIClient

        app = web.Application()

        if "GET" in methods:
            app.router.add_get(path, handler)
        if "POST" in methods:
            app.router.add_post(path, handler)
        if "PUT" in methods:
            app.router.add_put(path, handler)
        if "PATCH" in methods:
            app.router.add_patch(path, handler)
        if "DELETE" in methods:
            app.router.add_delete(path, handler)

        server = await aiohttp_server(app)

        api_client = DjangoAPIClient()
        api_client.base_url = f"http://{server.host}:{server.port}/api"
        return api_client

    return factory
