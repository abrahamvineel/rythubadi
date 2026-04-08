from typing import TypedDict, Optional
from uuid import UUID
from domain.regional_context import RegionalContext
from domain.language import Language
from domain.producer_profile import ProducerProfile
from domain.scheme_chunk import SchemeChunk
from domain.scheme_match import SchemeMatch

class SchemeAdvisorState(TypedDict):
    producer_id: UUID
    region: RegionalContext
    language: Language
    question: str
    farmer_profile: Optional[ProducerProfile]
    scheme_chunks: Optional[list[SchemeChunk]]
    scheme_matches: Optional[list[SchemeMatch]]
    llm_response: Optional[str]
    tools_called: list
