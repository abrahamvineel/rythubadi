from typing import TypedDict, Optional
from domain.producer_type import ProducerType
from domain.regional_context import RegionalContext
from uuid import UUID
from application.ports.i_llm_client import ILLMClient

class AgentState(TypedDict):
    farmer_question: str
    recommendation: Optional[str]
    producer_id: UUID
    producer_type: ProducerType
    crop_type: str
    region: RegionalContext
    error_details: Optional[str]

def advise(agent_state: AgentState, llm_client: ILLMClient) -> AgentState:
    response = llm_client.generate(agent_state['farmer_question'])
    if response == "":
            return {**agent_state, "recommendation": "Unable to get recommendation right now, "
        " Based on your region and this time of season, here's what to consider while you wait: "
        "[general guidance]. You can also consult your local agricultural extension office", "error_details": "LLM response is empty"}
    return {**agent_state, "recommendation": response}
