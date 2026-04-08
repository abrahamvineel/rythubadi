from uuid import UUID
from domain.producer_profile import ProducerProfile
import uuid
from domain.producer_type import ProducerType

class StubProducerRepository:

    def find_by_id(self, producer_id: UUID) -> ProducerProfile:
         return ProducerProfile(uuid.uuid4(), frozenset({ProducerType.FARMER}), "farmer1")
    