from domain.market_listing import MarketListing
from uuid import UUID
from typing import Optional, Iterator
from contextlib import contextmanager
from datetime import datetime

class InMemoryMarketListingRepository:

    def __init__(self):
        self._store: dict[UUID, MarketListing] = {}

    def save(self, listing: MarketListing) -> None:
        self._store[listing.listing_id] = listing

    def find_by_id(self, listing_id: UUID) -> Optional[MarketListing]:
        return self._store.get(listing_id)
    
    def find_by_producer_id(self, producer_id: UUID) -> list[MarketListing]:
        return [
            listing for listing in self._store.values()
            if listing.producer_id == producer_id
        ]
    
    def find_active(self, limit: int, created_at: Optional[datetime], listing_id: Optional[UUID]) -> list[MarketListing]:
        active = [l for l in self._store.values() if l.is_active]
        if created_at is None:
            sorted_active = sorted(active, key=lambda l: l.created_at, reverse=True)
            return sorted_active[:limit]
        
        older_than_created_at = [a for a in active if a.created_at < created_at]
        sorted_older_than_created_at = sorted(older_than_created_at, key=lambda l: l.created_at, reverse=True)
        return sorted_older_than_created_at[:limit]
    
    def find_all_active(self) -> list[MarketListing]:
        return [l for l in self._store.values() if l.is_active]
    
    def deactivate(self, listing_id: UUID) -> None:
        listing = self._store.get(listing_id)
        if listing:
            listing.is_active = False

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield 
