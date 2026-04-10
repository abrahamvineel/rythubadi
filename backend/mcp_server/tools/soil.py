from pydantic import BaseModel, Field
from mcp_server.server import mcp
from mcp_server.bootstrap import build_dependencies

_deps = build_dependencies()

class SoilInput(BaseModel):
    province_state: str = Field(..., min_length=2, max_length=100)

@mcp.tool()
def get_soil_moisture(province_state: str) -> dict:
    try:
        validated = SoilInput(province_state=province_state)
        soil_moisture = _deps.soil_moisture_provider.get_soil_moisture(validated.province_state)
        return {
            "moisture_pct": soil_moisture
        }
    except Exception as e:
        return {"error": "tool_failed", "detail": str(e)}
    