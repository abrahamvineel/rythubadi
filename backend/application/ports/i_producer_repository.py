from typing import Protocol, Optional
from uuid import UUID
from domain.producer_profile import ProducerProfile
from domain.producer_type import ProducerType

class IProducerRepository(Protocol):

    def find_by_id(self, producer_id: UUID) -> Optional[ProducerProfile]: ...

    def save(self, profile: ProducerProfile) -> None: ...

    def add_types(self, producer_id: UUID, new_types: frozenset[ProducerType]) -> ProducerProfile: ...
