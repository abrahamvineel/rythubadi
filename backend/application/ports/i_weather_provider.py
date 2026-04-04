from domain.weather_context import WeatherContext
from typing import Protocol

class IWeatherProvider(Protocol):

    def get_weather(self, province_state: str) -> WeatherContext: ...
