from dataclasses import dataclass
from uuid import UUID
from domain.producer_type import ProducerType


@dataclass(frozen=True)
class FarmLocation:
    id: UUID
    producer_id: UUID
    name: str
    latitude: float
    longitude: float
    producer_types: frozenset[ProducerType]
