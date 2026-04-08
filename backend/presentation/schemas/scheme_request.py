from pydantic import BaseModel, Field
from domain.language import Language
from uuid import UUID

class SchemeRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    producer_id: UUID
    province_state: str
    language: Language
    