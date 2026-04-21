from domain.weather_context import WeatherContext
from domain.data_precision import DataPrecision
from domain.regional_context import RegionalContext
import httpx

class OpenMeteoWeatherAdapter:

    _PROVINCE_CAPITALS: dict[str, str] = {
        # Canada
        "ontario": "Toronto", "british columbia": "Vancouver", "alberta": "Calgary",
        "quebec": "Montreal", "manitoba": "Winnipeg", "saskatchewan": "Regina",
        "nova scotia": "Halifax", "new brunswick": "Fredericton",
        "newfoundland": "St. John's", "prince edward island": "Charlottetown",
        # India
        "andhra pradesh": "Hyderabad", "telangana": "Hyderabad",
        "karnataka": "Bangalore", "tamil nadu": "Chennai",
        "maharashtra": "Mumbai", "gujarat": "Ahmedabad",
        "rajasthan": "Jaipur", "uttar pradesh": "Lucknow",
        "west bengal": "Kolkata", "punjab": "Chandigarh",
        # USA
        "california": "Los Angeles", "texas": "Houston",
        "new york": "New York City", "florida": "Miami",
        "illinois": "Chicago", "pennsylvania": "Philadelphia",
    }

    def _geocode(self, region: RegionalContext) -> tuple[float, float]:
        query = self._PROVINCE_CAPITALS.get(region.province_state.lower(), region.province_state)
        response = httpx.get("https://geocoding-api.open-meteo.com/v1/search",
                             params={"name": query, "count": 1})
        data = response.json()
        if not data.get("results"):
            raise ValueError(f"Unknown region: {region.province_state} ({region.country})")
        return (data["results"][0]["latitude"], data["results"][0]["longitude"])
    
    def get_weather(self, region: RegionalContext) -> WeatherContext:
        lat, lon = self._geocode(region=region)
        response = httpx.get("https://api.open-meteo.com/v1/forecast", 
                             params={
                                 "latitude":lat,
                                 "longitude":lon,
                                 "current":["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "uv_index", "surface_pressure", "visibility"],
                                 "daily":["temperature_2m_max", "temperature_2m_min"],
                                 "timezone":"auto"
                             })
        current = response.json()["current"]
        daily = response.json()["daily"]
        return WeatherContext(
            temperature=current["temperature_2m"],
            high_temperature=daily["temperature_2m_max"][0],
            low_temperature=daily["temperature_2m_min"][0],
            uv_index=int(current["uv_index"]),
            wind=current["wind_speed_10m"],
            precipitation=current["precipitation"],
            visibility=current["visibility"],
            pressure=current["surface_pressure"],
            humidity=current["relative_humidity_2m"],
            precision_level=DataPrecision.PROVINCE,
        )