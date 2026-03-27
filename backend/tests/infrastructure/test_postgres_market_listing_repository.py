import os
import uuid
import pytest
from decimal import Decimal
from datetime import datetime
from psycopg2.pool import ThreadedConnectionPool

from domain.market_listing import MarketListing
from domain.listing_mode import ListingMode
from domain.product import Product
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from infrastructure.postgres_market_listing_repository import PostgresMarketListingRepository


def make_listing(producer_id=None):
    return MarketListing(
        listing_id=uuid.uuid4(),
        listing_mode=ListingMode.SELL,
        price=Decimal("10.00"),
        product=Product(ProductCategory.GRAIN, PerishabilityLevel.LOW),
        created_at=datetime.now(),
        producer_id=producer_id or uuid.uuid4(),
        is_active=True,
        photo_url=None,
    )


@pytest.fixture
def repo():
    pool = ThreadedConnectionPool(1, 5, dsn=os.environ["TEST_DATABASE_URL"])
    repository = PostgresMarketListingRepository(pool)
    yield repository
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM market_listing")
        conn.commit()
    finally:
        pool.putconn(conn)
        pool.closeall()


@pytest.mark.integration
class TestPostgresMarketListingRepository:

    def test_save_success(self, repo):
        listing = make_listing()
        repo.save(listing)
        retrieved = repo.find_by_id(listing.listing_id)
        assert retrieved is not None
        assert retrieved.listing_id == listing.listing_id

    def test_find_by_id_returns_listing(self, repo):
        listing = make_listing()
        repo.save(listing)
        retrieved = repo.find_by_id(listing.listing_id)
        assert retrieved is not None
        assert retrieved.listing_id == listing.listing_id
        assert retrieved.price == listing.price
        assert retrieved.listing_mode == listing.listing_mode

    def test_find_by_id_returns_none_when_not_found(self, repo):
        retrieved = repo.find_by_id(uuid.uuid4())
        assert retrieved is None

    def test_find_by_producer_id_returns_only_their_listings(self, repo):
        producer_id = uuid.uuid4()
        repo.save(make_listing(producer_id=producer_id))
        repo.save(make_listing())
        results = repo.find_by_producer_id(producer_id)
        assert len(results) == 1
        assert results[0].producer_id == producer_id

    def test_find_by_producer_id_returns_empty_list_when_none(self, repo):
        results = repo.find_by_producer_id(uuid.uuid4())
        assert results == []

    def test_find_active_returns_paginated_results(self, repo):
        for _ in range(3):
            repo.save(make_listing())
        page1 = repo.find_active(page=1, page_size=2)
        page2 = repo.find_active(page=2, page_size=2)
        assert len(page1) == 2
        assert len(page2) == 1

    def test_find_active_excludes_inactive_listings(self, repo):
        listing = make_listing()
        repo.save(listing)
        repo.deactivate(listing.listing_id)
        results = repo.find_active(page=1, page_size=10)
        assert all(r.is_active for r in results)

    def test_find_all_active_returns_all_without_pagination(self, repo):
        for _ in range(3):
            repo.save(make_listing())
        inactive = make_listing()
        repo.save(inactive)
        repo.deactivate(inactive.listing_id)
        results = repo.find_all_active()
        assert len(results) == 3

    def test_deactivate_sets_is_active_false(self, repo):
        listing = make_listing()
        repo.save(listing)
        repo.deactivate(listing.listing_id)
        retrieved = repo.find_by_id(listing.listing_id)
        assert retrieved.is_active is False
