import httpx
from .config import WEATHER_API_BASE_URL, WEATHER_API_KEY
from .exceptions import WeatherAPIException, CityNotFoundException


async def fetch_weather(city: str):
    params = {"key": WEATHER_API_KEY, "q": city}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(WEATHER_API_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.RequestError:
        raise WeatherAPIException("Unable to connect to weather service.")
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 400:
            raise CityNotFoundException(f"City '{city}' not found.")
        elif exc.response.status_code == 404:
            raise CityNotFoundException(f"City '{city}' not found.")
        else:
            raise WeatherAPIException("Unexpected response from weather service.")
    except ValueError:
        raise WeatherAPIException("Invalid response format from weather service.")
    except Exception:
        raise WeatherAPIException("Weather service unavailable.")

    try:
        return {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_kph"],
            "condition": data["current"]["condition"]["text"]
        }
    except KeyError:
        raise WeatherAPIException("Incomplete data received from weather service.")
