from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    humidity: int
    wind_speed: float
    condition: str

class ErrorResponse(BaseModel):
    detail: str
