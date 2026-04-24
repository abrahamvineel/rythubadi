from application.services.market_listing_service import MarketListingService
from infrastructure.postgres_market_listing_repository import PostgresMarketListingRepository
from infrastructure.postgres_user_repository import PostgresUserRepository
from infrastructure.postgres_conversation_repository import PostgresConversationRepository
from psycopg2.pool import ThreadedConnectionPool
from infrastructure.llm.claude_client import ClaudeClient
from application.ports.i_llm_client import ILLMClient
import os
from functools import lru_cache
from dataclasses import dataclass
from langfuse import Langfuse
from infrastructure.llm.langfuse_claude_client import LangFuseClaudeClient
from infrastructure.stubs.stub_soil_moisture_provider import StubSoilMoistureProvider
from infrastructure.open_meteo_weather_adapter import OpenMeteoWeatherAdapter
from infrastructure.claude_image_analyzer import ClaudeImageAnalyzer
from infrastructure.stubs.stub_disease_corpus import StubDiseaseCorpus
from infrastructure.stubs.in_memory_confirmation_repository import InMemoryConfirmationRepository
from infrastructure.stubs.stub_producer_repository import StubProducerRepository
from application.agents.crop_advisor_graph import CropAdvisorGraph
from application.agents.crop_diagnosis_graph import CropDiagnosisGraph
from application.agents.scheme_advisor_graph import SchemeAdvisorGraph
from application.agents.orchestrator_graph import OrchestratorGraph
from langgraph.graph.state import CompiledStateGraph
from infrastructure.pgvector_scheme_repository import PgVectorSchemeRepository
from openai import OpenAI

@dataclass
class Services:
        market_listing: MarketListingService
        llm_client: ILLMClient
        crop_diagnosis_graph: CompiledStateGraph
        scheme_advisor_graph: CompiledStateGraph
        orchestrator_graph: CompiledStateGraph
        postgres_user_repo: PostgresUserRepository
        postgres_conversation_repo: PostgresConversationRepository

@lru_cache
def build_services():
        pool = ThreadedConnectionPool(2, 10, dsn=os.environ["DATABASE_URL"])
        repo = PostgresMarketListingRepository(pool)
        market_listing = MarketListingService(repo)
        openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        pgvector_scheme_repo = PgVectorSchemeRepository(pool, openai_client)

        llm_api_key = os.environ["ANTHROPIC_API_KEY"]
        claude_client = ClaudeClient(llm_api_key)

        llm_client = LangFuseClaudeClient(llm_client=claude_client, agent_name="crop_advisor")

        crop_advisor_graph = CropAdvisorGraph(llm_client=llm_client, weather_provider=OpenMeteoWeatherAdapter(), soil_moisture_provider=StubSoilMoistureProvider())
        
        crop_diagnosis_graph = CropDiagnosisGraph(llm_client=llm_client, weather_provider=OpenMeteoWeatherAdapter(), image_analyzer=ClaudeImageAnalyzer(api_key=llm_api_key), disease_corpus=StubDiseaseCorpus(), confirmation_repo=InMemoryConfirmationRepository())

        scheme_advisor_graph = SchemeAdvisorGraph(llm_client=llm_client, producer_repo=StubProducerRepository(), scheme_repo=pgvector_scheme_repo)

        orchestrator_graph = OrchestratorGraph(
                llm_client=llm_client,
                crop_advisor=crop_advisor_graph,
                crop_diagnosis=crop_diagnosis_graph,
                scheme_advisor=scheme_advisor_graph
        )

        postgres_user_repo = PostgresUserRepository(pool)

        postgres_conversation_repo = PostgresConversationRepository(pool)

        return Services(market_listing=market_listing, 
                        llm_client=llm_client,
                        crop_diagnosis_graph=crop_diagnosis_graph.build(), 
                        scheme_advisor_graph=scheme_advisor_graph.build(),
                        orchestrator_graph=orchestrator_graph.build(),
                        postgres_user_repo=postgres_user_repo,
                        postgres_conversation_repo=postgres_conversation_repo)
