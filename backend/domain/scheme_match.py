from dataclasses import dataclass, field
from domain.exceptions import InvalidConfidenceRangeError, EmptyReasonError

@dataclass(frozen=True)
class SchemeMatch:
    scheme_name: str
    eligible: bool
    reason: str
    confidence: float
    missing_criteria: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise InvalidConfidenceRangeError("Confidence not in range")
        if not self.reason:
            raise EmptyReasonError("Missing criteria is empty")
        