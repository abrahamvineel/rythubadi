from typing import Optional, TypedDict
from uuid import UUID
from domain.regional_context import RegionalContext
from domain.language import Language
from domain.producer_type import ProducerType

class OrchestratorState(TypedDict):
    farmer_message: str
    has_image:bool
    image_url: Optional[str]
    crop_type: Optional[str]
    producer_id: UUID
    producer_type: ProducerType
    region: RegionalContext
    language: Language
    routed_to: Optional[str]
    specialist_response: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    conversation_history: Optional[list]
