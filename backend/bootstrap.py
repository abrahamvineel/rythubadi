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
from infrastructure.stubs.stub_soil_moisture_provider import StubSoilMoistureProvider
from infrastructure.stubs.stub_weather_provider import StubWeatherProvider
from application.agents.crop_advisor_graph import CropAdvisorGraph
from langgraph.graph.state import CompiledStateGraph


@dataclass
class Services:
        market_listing: MarketListingService
        llm_client: ILLMClient
        crop_advisor_graph: CompiledStateGraph

@lru_cache
def build_services():
        pool = ThreadedConnectionPool(2, 10, dsn=os.environ["DATABASE_URL"])
        repo = PostgresMarketListingRepository(pool)
        market_listing = MarketListingService(repo)

        llm_api_key = os.environ["ANTHROPIC_API_KEY"]
        claude_client = ClaudeClient(llm_api_key)

        langfuse = Langfuse(public_key=os.environ["LANGFUSE_PUBLIC_KEY"], secret_key=os.environ["LANGFUSE_SECRET_KEY"])
        llm_client = LangFuseClaudeClient(llm_client=claude_client, langfuse=langfuse, agent_name="crop_advisor")

        crop_advisor_graph = CropAdvisorGraph(llm_client=llm_client, weather_provider=StubWeatherProvider(), soil_moisture_provider=StubSoilMoistureProvider())

        return Services(market_listing=market_listing, llm_client=llm_client, crop_advisor_graph=crop_advisor_graph.build())
