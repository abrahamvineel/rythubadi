from fastapi import APIRouter, Depends
from presentation.schemas.chat_request import ChatRequest
from presentation.schemas.chat_response import ChatResponse
from presentation.dependencies.auth import verify_clerk_jwt
from application.agents.orchestrator_state import OrchestratorState
from bootstrap import build_services
from domain.regional_context import RegionalContext

router = APIRouter()

@router.post("/chat", status_code=200)
def chat(request: ChatRequest, 
         token: str = Depends(verify_clerk_jwt)):
    agent_state = _build_agent_state(request)
    result = build_services().orchestrator_graph.invoke(agent_state)
    return ChatResponse(specialist_response=result["specialist_response"], routed_to=result["routed_to"])

def _build_agent_state(request: ChatRequest) -> OrchestratorState:
    return OrchestratorState(farmer_message   = request.message,
                            has_image        = request.image_url is not None,
                            image_url        = request.image_url,
                            crop_type        = request.crop_type,
                            producer_id      = request.producer_id,
                            producer_type    = request.producer_type,
                            region           = RegionalContext(request.province_state),
                            language         = request.language,
                            routed_to        = None,
                            specialist_response = None)
