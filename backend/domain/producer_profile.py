from dataclasses import dataclass
from uuid import UUID
from domain.exceptions import UnauthorisedOperationError, NoProducerTypeError, InvalidProducerTypeError
from domain.producer_type import ProducerType

@dataclass(frozen=True)
class ProducerProfile:
    producer_id: UUID
    producer_types: frozenset[ProducerType]
    name: str

    def __post_init__(self):
        if len(self.producer_types) == 0:
            raise NoProducerTypeError("Producer types are empty")
        elif all(not isinstance(types, ProducerType) for types in self.producer_types):
            raise InvalidProducerTypeError("Producer type is invalid")

    def check_ownership(self, requesting_producer_id: UUID) -> None:
        if requesting_producer_id != self.producer_id:
            raise UnauthorisedOperationError("Requesting producer id is not matching")
        