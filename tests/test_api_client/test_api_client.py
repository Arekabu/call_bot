from parser.exceptions import BaseServiceException, NetworkError, Server500

import pytest
from aiohttp import web


async def test_make_request_success(test_server_factory):
    """Тест успешных статусов 200, 201"""

    async def handler_200(request):
        return web.json_response({"data": "success"}, status=200)

    async def handler_201(request):
        return web.json_response({"data": "created"}, status=201)

    client_200 = await test_server_factory(handler_200, methods=["GET"])
    client_201 = await test_server_factory(handler_201, methods=["POST"])

    result_200 = await client_200._make_request("GET", "test")
    result_201 = await client_201._make_request("POST", "test")

    assert result_200 == {"data": "success"}
    assert result_201 == {"data": "created"}


async def test_make_request_500(test_server_factory):
    """Тест исключения 500"""

    async def handler_default(request):
        return web.json_response({}, status=500)

    async def handler_detail(request):
        return web.json_response({"detail": "Ошибка 500"}, status=500)

    client_default = await test_server_factory(handler_default, methods=["GET"])
    client_detail = await test_server_factory(handler_detail, methods=["GET"])

    with pytest.raises(Server500) as exc_info:
        await client_default._make_request("GET", "test")

    assert exc_info.value.send == "Внутренняя ошибка сервера. Попробуйте позже."

    with pytest.raises(Server500) as exc_info:
        await client_detail._make_request("GET", "test")

    assert exc_info.value.send == "Ошибка 500"


async def test_make_request_400(test_server_factory):
    """Тест исключения 400"""

    async def handler_default(request):
        return web.json_response({}, status=400)

    async def handler_detail(request):
        return web.json_response({"detail": "Bad Request"}, status=400)

    client_default = await test_server_factory(handler_default, methods=["GET"])
    client_detail = await test_server_factory(handler_detail, methods=["GET"])

    with pytest.raises(BaseServiceException) as exc_info:
        await client_default._make_request("GET", "test")

    assert exc_info.value.send == "Произошла ошибка. Попробуйте еще раз."

    with pytest.raises(BaseServiceException) as exc_info:
        await client_detail._make_request("GET", "test")

    assert exc_info.value.send == "Bad Request"


async def test_make_request_network_error(api_client):
    """Тест исключения NetworkError"""
    api_client.base_url = "http://invalid-host:9999"

    with pytest.raises(NetworkError) as exc_info:
        await api_client._make_request("GET", "test")

    assert "Network error:" in exc_info.value.send
