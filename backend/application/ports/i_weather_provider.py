from domain.weather_context import WeatherContext
from typing import Protocol
from domain.regional_context import RegionalContext
class IWeatherProvider(Protocol):

    def get_weather(self, region: RegionalContext) -> WeatherContext: ...
