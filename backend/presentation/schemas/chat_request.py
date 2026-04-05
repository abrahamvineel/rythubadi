from pydantic import BaseModel, Field
from uuid import UUID
from domain.producer_type import ProducerType
from domain.language import Language

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    producer_id: UUID
    crop_type: str
    province_state: str
    producer_type: ProducerType
    language: Language
    