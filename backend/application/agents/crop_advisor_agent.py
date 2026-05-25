from typing import TypedDict, Optional
from domain.producer_type import ProducerType
from domain.regional_context import RegionalContext
from uuid import UUID
from application.ports.i_llm_client import ILLMClient
from domain.weather_context import WeatherContext
from application.prompt_injection_guard import sanitise
from domain.language import Language

class AgentState(TypedDict):
    farmer_question: str
    recommendation: Optional[str]
    producer_id: UUID
    producer_type: ProducerType
    crop_type: str
    region: RegionalContext
    error_details: Optional[str]
    weather_context: Optional[WeatherContext]
    confidence: Optional[float]
    tools_called: list
    soil_moisture: Optional[float]
    data_disclaimer: Optional[str]
    language: Language
    lat: Optional[float]
    lon: Optional[float]
    conversation_history: Optional[list]
    loop_count: Optional[int]
    next_action: Optional[str]


def advise(agent_state: AgentState, llm_client: ILLMClient) -> AgentState:
    sanitise(agent_state["farmer_question"])
    
    # Track execution loops to avoid runaway bills
    current_loops = agent_state.get("loop_count") or 0
    updated_loops = current_loops + 1

    raw = llm_client.generate(_build_prompt(agent_state))
    parsed = _parse_response(raw)

    if parsed["type"] == "tool":
        # The LLM requested a tool call
        tool_name = parsed["value"]
        return {
            **agent_state,
            "next_action": tool_name,
            "loop_count": updated_loops
        }
    else:
        # The LLM output the final response
        recommendation = parsed["value"]
        confidence = parsed["confidence"]
        
        if not recommendation:
            return {
                **agent_state,
                "next_action": "respond",
                "recommendation": "Unable to get recommendation right now. Please consult local agronomists.",
                "confidence": 0.0,
                "loop_count": updated_loops,
                "error_details": "LLM response is empty"
            }
            
        return {
            **agent_state,
            "next_action": "respond",
            "recommendation": recommendation,
            "confidence": confidence,
            "loop_count": updated_loops
        }

def _build_prompt(agent_state: AgentState) -> list:
    crop_type = agent_state["crop_type"]
    province_state = agent_state["region"].province_state
    farmer_question = agent_state["farmer_question"]
    weather_context = agent_state["weather_context"]
    soil_moisture = agent_state["soil_moisture"]
    language = agent_state["language"].value
    tools_called = agent_state.get("tools_called") or []

    # System instruction guiding ReAct behaviour
    context_parts = [
        "You are an expert crop advisor.",
        f"Respond in {language}.",
        f"Farmer is growing {crop_type} in {province_state}.",
        "",
        "You have access to the following tools:",
        "1. weather: Returns current weather context (temperature, humidity).",
        "2. soil_moisture: Returns the current soil moisture percentage.",
        "",
        "CRITICAL: If you do not have weather or soil moisture data in your context but need them to answer, request them first.",
        "",
        "Formatting rules:",
        "- To call a tool, reply with exactly: TOOL: <tool_name> (e.g. 'TOOL: weather' or 'TOOL: soil_moisture').",
        "- Do not call a tool if you have already called it and have its data.",
        "- Once you have all the necessary information, output your final recommendation using this exact format:",
        "RESPONSE: <your recommendation here>",
        "CONFIDENCE: <decimal between 0.0 and 1.0>"
    ]

    # Dynamically feed the gathered tool data back into the prompt
    context_message = " ".join(context_parts)
    system_prompt = f"{context_message}\n\n=== Collected Data ==="
    
    if weather_context is not None:
        system_prompt += f"\n- Weather data: Temp {weather_context.temperature}°C, Humidity {weather_context.humidity}%."
    if soil_moisture is not None:
        system_prompt += f"\n- Soil moisture: {soil_moisture}%."
    if not weather_context and not soil_moisture:
        system_prompt += "\n- No tool data collected yet."

    history = agent_state.get("conversation_history") or []
    return [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": f"Question: {farmer_question}"}
    ]

def _parse_response(response: str) -> dict:
    cleaned = response.strip()
    
    # 1. Parse Tool Call
    if cleaned.startswith("TOOL:"):
        tool_name = cleaned.split("TOOL:", 1)[1].strip().lower()
        return {"type": "tool", "value": tool_name}

    # 2. Parse Final Response
    lines = cleaned.splitlines()
    recommendation_lines = []
    confidence = 0.5
    
    for line in lines:
        if line.startswith("RESPONSE:"):
            recommendation_lines.append(line.split("RESPONSE:", 1)[1].strip())
        elif line.startswith("CONFIDENCE:"):
            try:
                confidence = float(line.split("CONFIDENCE:", 1)[1].strip())
            except ValueError:
                pass
        else:
            if recommendation_lines:  # Capture multiline response content
                recommendation_lines.append(line)

    recommendation = "\n".join(recommendation_lines).strip()
    
    # Fallback parser if LLM failed to write prefixes but wrote confidence
    if not recommendation and lines:
        if lines[-1].startswith("CONFIDENCE:"):
            recommendation = "\n".join(lines[:-1]).strip()
        else:
            recommendation = cleaned

    return {"type": "response", "value": recommendation, "confidence": confidence}
