from fastapi import APIRouter, Depends
from presentation.schemas.chat_request import ChatRequest
from presentation.schemas.chat_response import ChatResponse
from presentation.dependencies.auth import verify_clerk_jwt
from application.agents.crop_advisor_agent import AgentState
from bootstrap import build_services
from domain.regional_context import RegionalContext

router = APIRouter()

@router.post("/chat", status_code=200)
def chat(request: ChatRequest, 
         token: str = Depends(verify_clerk_jwt)):
    agent_state = _build_agent_state(request)
    
    result = build_services().crop_advisor_graph.invoke(agent_state)

    return ChatResponse(recommendation=result["recommendation"], data_disclaimer=result["data_disclaimer"], routed_to_agronomist=(result["confidence"] or 0)< 0.7)

def _build_agent_state(request: ChatRequest) -> AgentState:
    return AgentState(farmer_question=request.message,
                      recommendation=None, 
                      producer_id=request.producer_id, 
                      producer_type=request.producer_type,
                      crop_type=request.crop_type, 
                      region=RegionalContext(request.province_state), 
                      error_details=None,
                      weather_context=None,
                      confidence=None,
                      tools_called=[],
                      soil_moisture=None,
                      data_disclaimer=None)
