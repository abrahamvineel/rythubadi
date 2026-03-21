from dataclasses import dataclass
from uuid import UUID
from domain.exceptions import UnauthorisedOperationError
from domain.producer_type import ProducerType

@dataclass(frozen=True)
class ProducerProfile:
    producer_id: UUID
    producer_type: ProducerType
    name: str

    def check_ownership(self, requesting_producer_id: UUID) -> None:
        if requesting_producer_id != self.producer_id:
            raise UnauthorisedOperationError("Requesting producer id is not matching")
        