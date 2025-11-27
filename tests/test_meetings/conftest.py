import pytest
from aiohttp import web


async def mock_meetings_handler(request):
    return web.json_response(
        {
            "meetings": [
                {
                    "title": "Test Meeting",
                    "meeting_time": "10:00 - 11:00",
                    "url": "https://test.meet/123",
                }
            ]
        }
    )


@pytest.fixture
async def meetings_api(aiohttp_server):
    """Фикстура тестового API клиента для meetings"""
    app = web.Application()
    app.router.add_get("/api/meetings", mock_meetings_handler)
    server = await aiohttp_server(app)
    return server


@pytest.fixture
async def meetings_service():
    """Фикстура для MeetingsService"""
    from services.meetings import MeetingsService

    return MeetingsService()
