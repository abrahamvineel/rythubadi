from typing import Protocol
from uuid import UUID
from domain.farm_location import FarmLocation


class ILocationRepository(Protocol):

    def find_by_producer(self, producer_id: UUID) -> list[FarmLocation]: ...

    def save(self, location: FarmLocation) -> None: ...

    def delete(self, location_id: UUID, producer_id: UUID) -> None: ...
