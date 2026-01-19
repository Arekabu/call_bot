async def test_get_meetings_success(meetings_api, mock_callback, meetings_service):
    """Тест успешного получения созвонов"""
    # Меняем base_url
    meetings_service.api.base_url = (
        f"http://{meetings_api.host}:{meetings_api.port}/api"
    )

    # Вызываем метод
    await meetings_service(callback=mock_callback)

    # Проверяем поля в ответе
    mock_callback.message.answer.assert_called_once()
    text = mock_callback.message.answer.call_args[0][0]

    assert "Test Meeting 01" in text
    assert "10:00" in text
    assert "11:00" in text
    assert "https://test.meet/123" in text

    assert "Test Meeting 02" in text
    assert "12:00" in text
    assert "13:00" in text
    assert "Ссылка не предоставлена." in text
