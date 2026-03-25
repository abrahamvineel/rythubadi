from domain.market_listing import MarketListing
from uuid import UUID
from typing import Optional, Iterator
from contextlib import contextmanager

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
    
    def find_active(self, page: int, page_size: int) -> list[MarketListing]:
        active = [l for l in self._store.values() if l.is_active]
        start = (page - 1) * page_size
        return active[start: start + page_size]
    
    def find_all_active(self) -> list[MarketListing]:
        return [l for l in self._store.values() if l.is_active]
    
    def deactivate(self, listing_id: UUID) -> None:
        listing = self._store.get(listing_id)
        if listing:
            listing.is_active = False

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield 
