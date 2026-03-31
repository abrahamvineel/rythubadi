from tests.fakes.in_memory_market_listing_repository import InMemoryMarketListingRepository
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.product import Product
from domain.listing_mode import ListingMode
from datetime import datetime
from decimal import Decimal
from domain.market_listing import MarketListing
from application.services.market_listing_service import MarketListingService
import pytest
from domain.exceptions import ListingNotFoundError
import uuid

class TestMarketListingService:

    def test_create_listing_success(self):

        repo = InMemoryMarketListingRepository()
        service = MarketListingService(repo)

        service.create_listing(
            listing_mode = ListingMode.SELL,
            price=Decimal('50'),
            product=Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL),
            producer_id=uuid.uuid4(),
            photo_url="test"
        )

        active = repo.find_active(limit=10, created_at=None, listing_id=None)
        assert len(active) == 1
        assert active[0].listing_mode == ListingMode.SELL

    def test_run_donation_sweep(self):
        repo = InMemoryMarketListingRepository()

        service = MarketListingService(repo)
        old_time = datetime(2024, 1, 1, 0, 0, 0)

        listing = MarketListing(
            uuid.uuid4(), ListingMode.SELL, Decimal('50'),
            Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL),
            old_time, uuid.uuid4(), True, "None"
        )
        repo.save(listing)

        service.run_donation_sweep(current_time=datetime.now())

        old = repo.find_by_id(listing.listing_id)

        assert old.is_active == False
        active = repo.find_active(limit=10, created_at=None, listing_id=None)
        assert len(active) == 1
        assert active[0].listing_mode == ListingMode.DONATE
    
    def test_get_active_listings_given_cursor_returns_older_listings(self):
        listing1 = MarketListing(
            uuid.uuid4(), ListingMode.SELL, Decimal('50'),
            Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL),
            datetime(2024, 1, 1, 0, 0, 0), uuid.uuid4(), True, "None"
        )

        listing2 = MarketListing(
            uuid.uuid4(), ListingMode.SELL, Decimal('50'),
            Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL),
            datetime(2024, 2, 1, 0, 0, 0), uuid.uuid4(), True, "None"
        )

        listing3 = MarketListing(
            uuid.uuid4(), ListingMode.SELL, Decimal('50'),
            Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL),
            datetime(2024, 3, 1, 0, 0, 0), uuid.uuid4(), True, "None"
        )

        repo = InMemoryMarketListingRepository()

        service = MarketListingService(repo)
        repo.save(listing1)
        repo.save(listing2)
        repo.save(listing3)

        active_listings = service.get_active_listings_for_cursor(5, datetime(2024, 2, 1, 0, 0, 0), listing2.listing_id)

        assert len(active_listings) == 1
        assert active_listings[0].listing_id == listing1.listing_id
        assert active_listings[0].created_at == listing1.created_at

    def test_get_market_listing_by_id_success(self):
        listing = MarketListing(
            uuid.uuid4(), ListingMode.SELL, Decimal('50'),
            Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL),
            datetime(2024, 1, 1, 0, 0, 0), uuid.uuid4(), True, "None"
        )
        repo = InMemoryMarketListingRepository()

        service = MarketListingService(repo)
        repo.save(listing)

        active_listing = service.get_listing_by_id(listing.listing_id)

        assert active_listing.listing_id == listing.listing_id

    def test_market_listing_by_id_raises_execption_on_no_listings(self):
        repo = InMemoryMarketListingRepository()
        service = MarketListingService(repo)
        with pytest.raises(ListingNotFoundError):
            service.get_listing_by_id(uuid.uuid4())
