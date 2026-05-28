from typing import Protocol
from uuid import UUID

class INotificationPort(Protocol):

    def send(self, producer_id: UUID, message: str, language: str) -> None: ...
    