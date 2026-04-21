from pydantic import BaseModel, Field
from uuid import UUID
from domain.producer_type import ProducerType
from domain.language import Language
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    producer_id: UUID
    crop_type: str
    province_state: str
    country: str = "CA"
    producer_type: ProducerType
    language: Language
    image_url: Optional[str]
    lat: Optional[float] = None
    lon: Optional[float] = None
    