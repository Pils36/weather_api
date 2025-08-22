from fastapi import FastAPI, Query, status, Request
from fastapi.responses import JSONResponse
from .schemas import WeatherResponse, ErrorResponse
from .weather_service import fetch_weather
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import WeatherAPIException, CityNotFoundException

app = FastAPI(title="Weather API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(CityNotFoundException)
async def city_not_found_handler(request: Request, exc: CityNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(WeatherAPIException)
async def weather_api_exception_handler(request: Request, exc: WeatherAPIException):
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Weather API. Use /weather endpoint to get weather data."}

@app.get("/weather", response_model=WeatherResponse, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}})
async def get_weather(city: str = Query(..., description="City name to fetch weather for")):
    weather_data = await fetch_weather(city)
    return weather_data
