from domain.weather_context import WeatherContext
from domain.data_precision import DataPrecision

class StubWeatherProvider:
    
    def get_weather(self, province_state: str) -> WeatherContext:
        return WeatherContext(23.0, 23.0, 18.0, None, None, 10.9, None, None, 78.3, DataPrecision.DISTRICT)
