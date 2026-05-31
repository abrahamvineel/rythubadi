import httpx
from infrastructure.open_meteo_weather_adapter import OpenMeteoWeatherAdapter
from domain.regional_context import RegionalContext

# Open-Meteo hourly soil moisture variable (0–7 cm depth).
# Returns m³/m³ volumetric water content — multiply by 100 → percentage.
# No API key required.

class OpenMeteoSoilAdapter:
    """
    Last-resort soil moisture fallback using the Open-Meteo forecast API.
    Reuses the existing geocoding logic from OpenMeteoWeatherAdapter.
    Returns the most recent hourly soil moisture at 0–7 cm depth as a
    0–100 percentage.
    """

    def __init__(self):
        self._geocoder = OpenMeteoWeatherAdapter()

    def get_soil_moisture(self, province_state: str) -> float:
        region = RegionalContext(province_state=province_state, country="")
        lat, lon = self._geocoder._geocode(region)

        response = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude":  lat,
                "longitude": lon,
                "hourly":    "soil_moisture_0_to_7cm",
                "timezone":  "auto",
                "forecast_days": 1,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

        # Take the first non-None hourly value
        values = data["hourly"]["soil_moisture_0_to_7cm"]
        value_m3 = next((v for v in values if v is not None), None)
        if value_m3 is None:
            raise ValueError("Open-Meteo returned no soil moisture values")

        pct = round(float(value_m3) * 100, 2)
        if not (0.0 <= pct <= 100.0):
            raise ValueError(f"Open-Meteo soil moisture out of range: {pct}")

        return pct
