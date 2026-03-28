from application.services.market_listing_service import MarketListingService
from infrastructure.postgres_market_listing_repository import PostgresMarketListingRepository
from psycopg2.pool import ThreadedConnectionPool
import os
from functools import lru_cache

@lru_cache
def build_services():
        pool = ThreadedConnectionPool(2, 10, dsn=os.environ["DATABASE_URL"])
        repo = PostgresMarketListingRepository(pool)
        return MarketListingService(repo)
