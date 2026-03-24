from backend.application.ports.i_market_listing_repository import IMarketListingRepository
from backend.domain.listing_mode import ListingMode
from backend.domain.market_listing import MarketListing
from backend.domain.exceptions import InvalidPriceError, InvalidListingModeError
from backend.domain.product_category import ProductCategory
from backend.domain.producer_profile import ProducerProfile
from backend.domain.producer_type import ProducerType
from backend.domain.perishability_level import PerishabilityLevel
from backend.domain.product import Product
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
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

    def deactivate(self, listing_id: UUID) -> None:
        listing = self._store.get(listing_id)
        if listing:
            listing.is_active = False

    @contextmanager
    def transaction(self) -> Iterator[None]:
        yield 


    # def test_save_and_find_by_id(self):
    #     repo = InMemoryMarketListingRepository()
    #     product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
    #     listing_id = uuid4()
    #     listing_mode = ListingMode.DONATE
    #     price = Decimal('0.0')
    #     created_at = datetime.now()
    #     listing = MarketListing(listing_id, listing_mode, price, product, created_at, uuid4(), True)

    #     repo.save(listing)

    #     result = repo.find_by_id(listing.listing_id)
    #     assert result == listing

    # def test_find_by_producer_id_returns_only_that_prodcers_listings(self):
    #     repo = InMemoryMarketListingRepository()
    #     producer_a = uuid4()
    #     producer_b = uuid4()

    #     product_a = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
    #     listing_id_a = uuid4()
    #     listing_mode_a = ListingMode.DONATE
    #     price_a = Decimal('0.0')
    #     created_at_a = datetime.now()
    #     listing_a = MarketListing(listing_id_a, listing_mode_a, price_a, product_a, created_at_a, producer_a., True)

    #     product_b = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
    #     listing_id_b = uuid4()
    #     listing_mode_b = ListingMode.DONATE
    #     price_b = Decimal('0.0')
    #     created_at_b = datetime.now()
    #     listing_b = MarketListing(listing_id_b, listing_mode_b, price_b, product_b, created_at_b, uuid.uuid4(), True)

    #     repo.save(listing_a)
    #     repo.save(listing_b)

    #     result = repo.find_by_producer_id(producer_a)
    #     assert len(result) == 1
    #     assert result[0].producer_id == producer_a
