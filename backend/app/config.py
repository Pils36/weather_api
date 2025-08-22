import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("WEATHER_API_BASE_URL")

if not WEATHER_API_KEY:
    raise ValueError("Missing environment variable: WEATHER_API_KEY")

if not BASE_URL:
    raise ValueError("Missing environment variable: WEATHER_API_BASE_URL")

WEATHER_API_BASE_URL = f"{BASE_URL}/current.json"
