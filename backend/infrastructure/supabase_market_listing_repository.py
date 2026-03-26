from domain.market_listing import MarketListing
from typing import Optional, Iterator
from uuid import UUID
from contextlib import contextmanager

class SupabaseMarketListingRepository:
    
    def __init__(self, client):
        self.client = client

    def save(self, listing: MarketListing) -> None:
        pass

    def find_by_id(self, listing_id: UUID) -> Optional[MarketListing]:
        pass

    def find_by_producer_id(self, producer_id: UUID) -> list[MarketListing]:
        pass
    
    def find_active(self, page: int, page_size: int) -> list[MarketListing]:
        pass
    
    def find_all_active(self) -> list[MarketListing]:
        pass

    def deactivate(self, listing_id: UUID) -> None:
        pass

    @contextmanager
    def transaction(self) -> Iterator[None]:
        try:
            yield 
            #commit
        except:
            #rollback
            raise
