from typing import TypedDict, Optional
from domain.producer_type import ProducerType
from domain.regional_context import RegionalContext
from uuid import UUID

class AgentState(TypedDict):
    farmer_question: str
    recommendation: Optional[str]
    producer_id: UUID
    producer_type: ProducerType
    crop_type: str
    region: RegionalContext
    error_details: Optional[str]
