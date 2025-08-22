class WeatherAPIException(Exception):
    def __init__(self, message="Weather API error"):
        self.message = message
        super().__init__(self.message)


class CityNotFoundException(WeatherAPIException):
    def __init__(self, message="City not found"):
        super().__init__(message)
