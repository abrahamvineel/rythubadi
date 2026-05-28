from typing import Protocol
from domain.sensor_reading import SensorReading
from uuid import UUID

class ISensorReadingRepository(Protocol):

    def save(self, reading: SensorReading) -> None: ...

    def find_recent(self, producer_id: UUID, limit: int) -> list[SensorReading]: ...

    def was_notified_recently(self, producer_id: UUID, topic: str, hours: int) -> bool: ...
