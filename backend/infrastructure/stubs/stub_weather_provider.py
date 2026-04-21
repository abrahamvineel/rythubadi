from domain.weather_context import WeatherContext
from domain.data_precision import DataPrecision
from domain.regional_context import RegionalContext

class StubWeatherProvider:
    
    def get_weather(self, region: RegionalContext) -> WeatherContext:
        return WeatherContext(23.0, 23.0, 18.0, None, None, 10.9, None, None, 78.3, DataPrecision.DISTRICT)
