async def test_async_works() -> None:
    """Проверяем что async работает"""

    async def dummy() -> str:
        return "ok"

    result = await dummy()
    assert result == "ok"
