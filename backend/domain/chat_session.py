from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class ChatSession:
    id: UUID
    title: str
    producer_id: str
    is_deleted: bool = False
    