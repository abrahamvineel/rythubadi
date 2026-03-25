from tests.fakes.in_memory_market_listing_repository import InMemoryMarketListingRepository
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.product import Product
from domain.listing_mode import ListingMode
from datetime import datetime
from decimal import Decimal
from domain.market_listing import MarketListing
from application.services.market_listing_service import MarketListingService
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

        active = repo.find_active(page=1, page_size=10)
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
        active = repo.find_active(page=1, page_size=10)
        assert len(active) == 1
        assert active[0].listing_mode == ListingMode.DONATE
        