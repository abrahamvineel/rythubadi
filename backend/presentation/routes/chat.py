from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from application.agents.crop_advisor_agent import AgentState, _build_prompt
from domain.language import Language
from presentation.schemas.chat_request import ChatRequest
from presentation.schemas.chat_response import ChatResponse
from presentation.dependencies.auth import get_current_user_id
from application.agents.orchestrator_state import OrchestratorState
from bootstrap import build_services
from domain.regional_context import RegionalContext
from typing import Optional
from application.prompt_injection_guard import sanitise

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
            for m in messages
        ]
    return history

@router.post("/chat/stream")
def stream(request: ChatRequest, 
           user_id: str = Depends(get_current_user_id)):
    def generate():
        services = build_services()
        history = _fetch_conversation_history(request)
        state = _build_agent_state(request)
        valid_set = ("crop_advisor", "crop_diagnosis", "scheme_advisor")
        sanitise(state["farmer_message"])
        region = RegionalContext(request.province_state, request.country)
        classify_prompt  = [
            {"role": "system", "content": "Classify the farmer's question. Reply with exactly one word: crop_advisor, crop_diagnosis, or scheme_advisor."},
            {"role": "user", "content": state["farmer_message"]}
            ]
        routed_to = services.llm_client.generate(classify_prompt).strip().lower()        
        if routed_to not in valid_set: routed_to = "crop_advisor"
        if routed_to == "crop_advisor":
            weather = services.weather_provider.get_weather(region, lat=request.lat, lon=request.lon)
            soil = services.soil_moisture_provider.get_soil_moisture(region.province_state)
            agent_state = AgentState(
                farmer_question=request.message,
                crop_type=request.crop_type,
                region=region,
                language=request.language,
                producer_id=request.producer_id,
                producer_type=request.producer_type,
                recommendation=None, confidence=None,
                weather_context=weather, 
                soil_moisture=soil,
                data_disclaimer=None, error_details=None,
                tools_called=[], lat=request.lat, lon=request.lon,
                conversation_history=history
            )
            prompt = _build_prompt(agent_state)
            for chunk in services.llm_client.stream(prompt):
                yield f"data: {chunk}\n\n".encode()
        else:
            result = services.orchestrator_graph.invoke(_build_agent_state(request))
            yield f"data: {result['specialist_response']}\n\n".encode()
        yield "data: [DONE]\n\n".encode()
    return StreamingResponse(generate(), media_type="text/event-stream")
