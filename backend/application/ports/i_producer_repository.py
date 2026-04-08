from typing import Protocol
from uuid import UUID
from domain.producer_profile import ProducerProfile

class IProducerRepository(Protocol):

    def find_by_id(self, producer_id: UUID) -> ProducerProfile: ...
    