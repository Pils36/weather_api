import pytest
from httpx import AsyncClient, Request, HTTPStatusError, ASGITransport, RequestError
from app.main import app
from app.weather_service import WEATHER_API_BASE_URL

@pytest.mark.asyncio
async def test_successful_weather_fetch(mocker):
    mock_response = {
        "location": {"name": "London"},
        "current": {
            "temp_c": 20.5,
            "humidity": 65,
            "wind_kph": 10.2,
            "condition": {"text": "Sunny"}
        }
    }

    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return mock_response
            def raise_for_status(self):
                pass
        return MockResponse()

    mocker.patch("httpx.AsyncClient.get", side_effect=mock_get)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/weather", params={"city": "London"})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['current']["temp_c"], float)
    assert data['current']["temp_c"] == 20.5
    assert data['current']["humidity"] == 65
    assert data['current']["wind_kph"] == 10.2
    assert data['current']["condition"]["text"] == "Sunny"

@pytest.mark.asyncio
async def test_city_not_found(mocker):
    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 404
            def json(self):
                return {"detail": "City not found"}
            def raise_for_status(self):
                request = Request("GET", WEATHER_API_BASE_URL)
                raise HTTPStatusError("Not Found", request=request, response=self)
        return MockResponse()

    mocker.patch("httpx.AsyncClient.get", side_effect=mock_get)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/weather", params={"city": "UnknownCity"})

    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"