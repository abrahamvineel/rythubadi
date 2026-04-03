from application.services.market_listing_service import MarketListingService
from infrastructure.postgres_market_listing_repository import PostgresMarketListingRepository
from psycopg2.pool import ThreadedConnectionPool
from infrastructure.llm.claude_client import ClaudeClient
import os
from functools import lru_cache
from dataclasses import dataclass

@dataclass
class Services:
        market_listing: MarketListingService
        llm_client: ClaudeClient


@lru_cache
def build_services():
        pool = ThreadedConnectionPool(2, 10, dsn=os.environ["DATABASE_URL"])
        repo = PostgresMarketListingRepository(pool)
        market_listing = MarketListingService(repo)

        llm_api_key = os.environ["ANTHROPIC_API_KEY"]
        claude_client = ClaudeClient(llm_api_key)
        return Services(market_listing=market_listing, llm_client=claude_client)
