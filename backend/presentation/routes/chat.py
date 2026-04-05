from fastapi import APIRouter, Depends
from presentation.schemas.chat_request import ChatRequest
from presentation.schemas.chat_response import ChatResponse
from presentation.dependencies.auth import verify_clerk_jwt
from application.agents.crop_advisor_agent import AgentState
from bootstrap import build_services

router = APIRouter()

@router.post("/chat", status_code=201)
def chat(request: ChatRequest, 
         token: str = Depends(verify_clerk_jwt)):
    agent_state = AgentState(request["message"], 
                             request["producer_id"],
                             request["crop_type"],
                             request["producer_type"],
                             request["province_state"])
    
    result = build_services().crop_advisor_graph(agent_state)

    return ChatResponse(recommendation=result["recommendation"], data_disclaimer=result["data_disclaimer"], routed_to_agronomist=result["agronomist"])
