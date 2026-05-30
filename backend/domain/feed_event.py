from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class FeedEvent:
    id: UUID
    producer_id: UUID
    severity: str           # 'info' | 'warning' | 'alert'
    agent: str
    agent_emoji: str
    title: str
    body: str
    subject_type: str | None
    subject_id: str | None
    subject_name: str | None
    location_id: UUID | None
    reply_count: int
    created_at: datetime
