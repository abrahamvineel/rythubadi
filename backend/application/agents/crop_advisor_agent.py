from typing import TypedDict, Optional
from domain.producer_type import ProducerType
from domain.regional_context import RegionalContext
from uuid import UUID
from application.ports.i_llm_client import ILLMClient
from domain.weather_context import WeatherContext

class AgentState(TypedDict):
    farmer_question: str
    recommendation: Optional[str]
    producer_id: UUID
    producer_type: ProducerType
    crop_type: str
    region: RegionalContext
    error_details: Optional[str]
    weather_context: Optional[WeatherContext]

def advise(agent_state: AgentState, llm_client: ILLMClient) -> AgentState:
    response = llm_client.generate(_build_prompt(agent_state))
    if response == "":
            return {**agent_state, "recommendation": "Unable to get recommendation right now, "
        " Based on your region and this time of season, here's what to consider while you wait: "
        "[general guidance]. You can also consult your local agricultural extension office", "error_details": "LLM response is empty"}
    return {**agent_state, "recommendation": response}

def _build_prompt(agent_state: AgentState) -> str:
    crop_type = agent_state["crop_type"]
    province_state = agent_state["region"].province_state
    farmer_question = agent_state["farmer_question"]
    weather_context = agent_state["weather_context"]

    if weather_context is not None:
        return (
            f"You are a crop advisor. Farmer is growing {crop_type} in {province_state}. "
            f"Temperature: {weather_context.temperature}°C, Humidity: {weather_context.humidity}%. "
            f"Data precision: {weather_context.precision_level.value}. "
            f"Question: {farmer_question}"
        )

    return (
        f"You are a crop advisor. Farmer is growing {crop_type} in {province_state}. "
        f"Weather data is unavailable. "
        f"Question: {farmer_question}"
    )
