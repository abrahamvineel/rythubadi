from pydantic import BaseModel, Field
from mcp_server.server import mcp

class CropInput(BaseModel):
    crop_type: str = Field(..., min_length=2, max_length=100)
    planting_date: str = Field(..., min_length=8, max_length=10)

# TODO: replace with real crop stage adapter
@mcp.tool()
def get_crop(crop_type: str, planting_date: str) -> dict:
    try:
        validated = CropInput(crop_type=crop_type, planting_date=planting_date)
        return {"crop_type": crop_type, 
                "planting_date": planting_date, 
                "stage": "vegetative", 
                "days_since_planting": 85
            }

    except Exception as e:
        return {"error": "tool_failed", "detail": str(e)}
    