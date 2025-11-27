from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiohttp import web

from services.registration import RegistrationService


async def test_process_email(test_server_factory, mock_message):
    """Тест эндпойнта api/users/email"""

    async def handler(request):
        return web.json_response({}, status=200)

    async def handler_error(request):
        return web.json_response({"detail": "Это не email!"}, status=400)

    client = RegistrationService()
    client_error = RegistrationService()

    client.api_client = await test_server_factory(
        handler, path="/api/users/email", methods=["POST"]
    )
    client_error.api_client = await test_server_factory(
        handler_error, path="/api/users/email", methods=["POST"]
    )

    mock_message.text = "test@example.com"
    mock_state = AsyncMock(spec=FSMContext)

    await client.process_email(mock_message, mock_state)

    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[0][0]
    assert "Введите код, отправленный на email: test@example.com" in text

    mock_message.answer.reset_mock()

    await client_error.process_email(mock_message, mock_state)

    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[0][0]
    assert "Это не email!" in text


async def test_process_code(test_server_factory, mock_message):
    """Тест эндпойнта api/users/code"""

    async def handler(request):
        return web.json_response({"confirm": "Пользователь активирован"}, status=201)

    async def handler_error(request):
        return web.json_response({"detail": "Неверный код."}, status=401)

    client = RegistrationService()
    client_error = RegistrationService()

    client.api_client = await test_server_factory(
        handler, path="/api/users/code", methods=["POST"]
    )
    client_error.api_client = await test_server_factory(
        handler_error, path="/api/users/code", methods=["POST"]
    )

    mock_message.text = "1234"
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.get_data.return_value = {
        "email": "test@example.com",
        "telegram_id": "123456",
    }

    await client.process_code(mock_message, mock_state)
    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[0][0]

    assert "Пользователь активирован" in text

    mock_message.answer.reset_mock()

    await client_error.process_code(mock_message, mock_state)
    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[0][0]

    assert "Неверный код." in text
