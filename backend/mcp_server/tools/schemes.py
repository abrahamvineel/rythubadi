from pydantic import BaseModel, Field
from mcp_server.server import mcp
from mcp_server.bootstrap import build_dependencies
from domain.regional_context import RegionalContext

_deps = build_dependencies()

class SchemesInput(BaseModel):
    province_state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="CA", min_length=2, max_length=10)
    crop_type: str = Field(..., min_length=2, max_length=100)

@mcp.tool()
def get_schemes(province_state: str, crop_type: str, country: str = "CA") -> dict:
    try:
        validated = SchemesInput(province_state=province_state, crop_type=crop_type, country=country)
        schemes = _deps.scheme_repository.search(query=validated.crop_type,
                                                 regional_context=RegionalContext(validated.province_state, validated.country),
                                                 top_k=5)
        return [{"title": s.scheme_name, 
                 "description": s.content, 
                 "source_url": s.source_url, 
                 "relevance_score": s.similarity_score} for s in schemes]

    except Exception as e:
        return {"error": "tool_failed", "detail": str(e)}
    