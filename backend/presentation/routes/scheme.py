from fastapi import APIRouter, Depends
from presentation.schemas.scheme_request import SchemeRequest
from presentation.schemas.scheme_response import SchemeResponse
from presentation.dependencies.auth import verify_clerk_jwt
from application.agents.scheme_advisor_state import SchemeAdvisorState
from domain.regional_context import RegionalContext
from bootstrap import build_services

router = APIRouter()

@router.post("/scheme", status_code=200)
def scheme_router(request: SchemeRequest,
                  token = Depends(verify_clerk_jwt)):
    scheme_advisor_agent = _build_scheme_advisor_agent(request)
    result = build_services().scheme_advisor_graph.invoke(scheme_advisor_agent)
    return SchemeResponse(response=result["llm_response"], tools_called=result["tools_called"])

def _build_scheme_advisor_agent(request: SchemeRequest):
    return SchemeAdvisorState(
        producer_id=request.producer_id,
        region=RegionalContext(request.province_state),
        language=request.language,
        question=request.question,
        farmer_profile=None,
        scheme_chunks=None,
        scheme_matches=None,
        llm_response=None,
        tools_called=[]
    )
