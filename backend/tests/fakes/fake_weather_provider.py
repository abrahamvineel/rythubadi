from domain.weather_context import WeatherContext

class FakeWeatherProvider:

    def __init__(self, weather_context: WeatherContext):
        self.weather_context = weather_context

    def get_weather(self, province_state: str) -> WeatherContext:
        return self.weather_context
    