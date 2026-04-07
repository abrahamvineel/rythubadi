from typing import Optional
from dataclasses import dataclass
from domain.exceptions import InvalidSimilarityScoreRangeError, EmptyContentError, EmptyCountryError

@dataclass(frozen=True)
class SchemeChunk:
    scheme_name: str
    content: str
    country: str
    province: Optional[str]
    source_url: str
    similarity_score: float

    def __post_init__(self):
        if self.similarity_score < 0.0 or self.similarity_score > 1.0:
            raise InvalidSimilarityScoreRangeError("Similarity score range is invalid")
        if not self.content:
            raise EmptyContentError("Content is empty")
        if not self.country:
            raise EmptyCountryError("Country is empty")
