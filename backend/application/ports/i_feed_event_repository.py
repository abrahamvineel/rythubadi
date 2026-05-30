from typing import Protocol
from uuid import UUID
from domain.feed_event import FeedEvent


class IFeedEventRepository(Protocol):
    def find_by_producer(self, producer_id: UUID, limit: int = 50) -> list[FeedEvent]: ...
    def save(self, event: FeedEvent) -> None: ...
