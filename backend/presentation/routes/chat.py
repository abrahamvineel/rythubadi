from fastapi import APIRouter, Depends
from presentation.schemas.chat_request import ChatRequest
from presentation.schemas.chat_response import ChatResponse
from presentation.dependencies.auth import get_current_user_id
from application.agents.orchestrator_state import OrchestratorState
from bootstrap import build_services
from domain.regional_context import RegionalContext
from typing import Optional

router = APIRouter()

@router.post("/chat", status_code=200)
def chat(request: ChatRequest, 
         user_id: str = Depends(get_current_user_id)):
    agent_state = _build_agent_state(request)
    result = build_services().orchestrator_graph.invoke(agent_state)
    return ChatResponse(specialist_response=result["specialist_response"], routed_to=result["routed_to"])

def _build_agent_state(request: ChatRequest) -> OrchestratorState:
    return OrchestratorState(farmer_message      = request.message,
                            has_image            = request.image_url is not None,
                            image_url            = request.image_url,
                            crop_type            = request.crop_type,
                            producer_id          = request.producer_id,
                            producer_type        = request.producer_type,
                            region               = RegionalContext(request.province_state, request.country),
                            language             = request.language,
                            routed_to            = None,
                            specialist_response  = None,
                            lat                  = request.lat,
                            lon                  = request.lon,
                            conversation_history =_fetch_conversation_history(request=request))

def _fetch_conversation_history(request: ChatRequest) -> Optional[list]:
    history = []
    if request.conversation_id:
        messages = build_services().postgres_conversation_repo.find_messages_by_session(request.conversation_id)
        history = [
            {"role": "assistant" if m.system_generated else "user", "content": m.content}
            for m in messages[-10:]
        ]
    return history

