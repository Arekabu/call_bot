async def test_get_meetings_success(meetings_api, mock_message, meetings_service):
    """Тест успешного получения созвонов"""
    # Меняем base_url
    meetings_service.api_client.base_url = (
        f"http://{meetings_api.host}:{meetings_api.port}/api"
    )

    # Вызываем метод
    await meetings_service.get_meetings(mock_message)

    # Проверяем поля в ответе
    mock_message.answer.assert_called_once()
    text = mock_message.answer.call_args[0][0]

    assert "Test Meeting" in text
    assert "10:00" in text
    assert "11:00" in text
    assert "https://test.meet/123" in text
