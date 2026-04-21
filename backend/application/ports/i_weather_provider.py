from domain.weather_context import WeatherContext
from typing import Protocol, Optional
from domain.regional_context import RegionalContext

class IWeatherProvider(Protocol):

    def get_weather(self, region: RegionalContext, lat: Optional[float] = None, lon: Optional[float] = None) -> WeatherContext: ...
