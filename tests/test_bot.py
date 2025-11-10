import pytest


@pytest.mark.asyncio
async def test_async_works():
    """Проверяем что async работает"""

    async def dummy():
        return "ok"

    result = await dummy()
    assert result == "ok"
