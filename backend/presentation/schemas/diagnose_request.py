from uuid import UUID
from domain.language import Language
from pydantic import BaseModel, Field

class DiagnoseRequest(BaseModel):
    image_url: str = Field(..., min_length=1)
    crop_type: str
    province_state: str
    country: str = "CA"
    producer_id: UUID
    language: Language
