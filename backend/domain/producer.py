from dataclasses import dataclass
from uuid import UUID
from domain.exceptions import UnauthorisedOperationError
from domain.producer_type import ProducerType

@dataclass(frozen=True)
class ProducerProfile:
    producer_id: UUID
    producer_type: ProducerType
    name: str
