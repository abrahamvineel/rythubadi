from domain.weather_context import WeatherContext
from domain.regional_context import RegionalContext

class FakeWeatherProvider:

    def __init__(self, weather_context: WeatherContext):
        self.weather_context = weather_context

    def get_weather(self, region: RegionalContext) -> WeatherContext:
        return self.weather_context
    