from pydantic import BaseModel, Field, field_validator
from mcp_server.server import mcp
from mcp_server.bootstrap import build_dependencies

_deps = build_dependencies()

class ImageAnalyseInput(BaseModel):
    image_url: str = Field(..., min_length=10, max_length=500)
    crop_type: str = Field(..., min_length=2, max_length=100)

    @field_validator("image_url")
    @classmethod
    def must_be_https(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError("image_url must use https")
        return v


@mcp.tool()
def get_image_analysis(image_url: str, crop_type: str) -> dict:
    try:
        validated = ImageAnalyseInput(image_url=image_url, crop_type=crop_type)
        diagnosis = _deps.image_analyzer.analyse_image(validated.image_url)
        return {
            "diagnosis": diagnosis,
            "crop_type": crop_type
        }
    except Exception as e:
        return {"error": "tool_failed", "detail": str(e)}
    