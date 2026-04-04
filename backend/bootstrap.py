from application.services.market_listing_service import MarketListingService
from infrastructure.postgres_market_listing_repository import PostgresMarketListingRepository
from psycopg2.pool import ThreadedConnectionPool
from infrastructure.llm.claude_client import ClaudeClient
from application.ports.i_llm_client import ILLMClient
import os
from functools import lru_cache
from dataclasses import dataclass
from langfuse import Langfuse
from infrastructure.llm.langfuse_claude_client import LangFuseClaudeClient

@dataclass
class Services:
        market_listing: MarketListingService
        llm_client: ILLMClient

@lru_cache
def build_services():
        pool = ThreadedConnectionPool(2, 10, dsn=os.environ["DATABASE_URL"])
        repo = PostgresMarketListingRepository(pool)
        market_listing = MarketListingService(repo)

        llm_api_key = os.environ["ANTHROPIC_API_KEY"]
        claude_client = ClaudeClient(llm_api_key)

        langfuse = Langfuse(public_key=os.environ["LANGFUSE_PUBLIC_KEY"], secret_key=os.environ["LANGFUSE_SECRET_KEY"])
        llm_client = LangFuseClaudeClient(llm_client=claude_client, langfuse=langfuse, agent_name="crop_advisor")

        return Services(market_listing=market_listing, llm_client=llm_client)
