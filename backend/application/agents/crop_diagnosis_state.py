from typing import TypedDict, Optional
from uuid import UUID
from domain.language import Language
from domain.regional_context import RegionalContext
from domain.weather_context import WeatherContext

class CropDiagnosisState(TypedDict):
        image_url: str
        crop_type: str
        region: RegionalContext
        language: Language
        producer_id: UUID
        weather_context: Optional[WeatherContext]
        disease_candidate: Optional[str]
        corpus_matches: Optional[list[str]]
        llm_diagnosis: Optional[str]
        confirmation_id: Optional[UUID]
        pending_confirmation: bool
        tools_called: list
        lat: Optional[float]
        lon: Optional[float]
        