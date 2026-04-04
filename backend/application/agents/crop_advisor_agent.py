from typing import TypedDict, Optional
from domain.producer_type import ProducerType
from domain.regional_context import RegionalContext
from uuid import UUID
from application.ports.i_llm_client import ILLMClient
from domain.weather_context import WeatherContext
from application.prompt_injection_guard import sanitise

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

def advise(agent_state: AgentState, llm_client: ILLMClient) -> AgentState:
    sanitise(agent_state["farmer_question"])
    response = llm_client.generate(_build_prompt(agent_state))
    if response == "":
            return {**agent_state, "recommendation": "Unable to get recommendation right now, "
        " Based on your region and this time of season, here's what to consider while you wait: "
        "[general guidance]. You can also consult your local agricultural extension office", "error_details": "LLM response is empty"}
    return {**agent_state, "recommendation": response}

def _build_prompt(agent_state: AgentState) -> list:
    crop_type = agent_state["crop_type"]
    province_state = agent_state["region"].province_state
    farmer_question = agent_state["farmer_question"]
    weather_context = agent_state["weather_context"]
    soil_moisture = agent_state["soil_moisture"]

    context_parts = [
        f"You are a crop advisor.",
        f"Farmer is growing {crop_type} in {province_state}."
    ]

    if weather_context is not None:
        context_parts.append(
            f"Temperature: {weather_context.temperature}°C, "
            f"Humidity: {weather_context.humidity}%."
        )

    if soil_moisture is not None:
        context_parts.append(f"Soil moisture: {soil_moisture}%.")

    return [
        {"role": "system", "content": " ".join(context_parts)},
        {"role": "user", "content": f"Question: {farmer_question}"}
    ]

