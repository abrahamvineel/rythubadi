from pydantic import BaseModel, Field
from mcp_server.server import mcp
from mcp_server.bootstrap import build_dependencies

_deps = build_dependencies()

from domain.regional_context import RegionalContext

class WeatherInput(BaseModel):
    province_state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="CA", min_length=2, max_length=10)
    crop_type: str = Field(..., min_length=2, max_length=100)

@mcp.tool()
def get_weather(province_state: str, crop_type: str, country: str = "CA") -> dict:
    try:
        validated = WeatherInput(province_state=province_state, crop_type=crop_type, country=country)
        weather = _deps.weather_provider.get_weather(RegionalContext(validated.province_state, validated.country))
        return {
            "temperature_c": weather.temperature,
            "humidity_pct": weather.humidity,
            "precipitation_mm": weather.precipitation,
            "precision_level": weather.precision_level.value
        }
    except Exception as e:
        return {"error": "tool_failed", "detail": str(e)}
    