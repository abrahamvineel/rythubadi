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
from infrastructure.stubs.stub_weather_provider import StubWeatherProvider
from infrastructure.stubs.stub_image_analyser import StubImageAnalyser
from infrastructure.stubs.stub_disease_corpus import StubDiseaseCorpus
from infrastructure.stubs.in_memory_confirmation_repository import InMemoryConfirmationRepository
from infrastructure.stubs.stub_producer_repository import StubProducerRepository
from infrastructure.stubs.stub_scheme_repository import StubSchemeRepository
from application.agents.crop_advisor_graph import CropAdvisorGraph
from application.agents.crop_diagnosis_graph import CropDiagnosisGraph
from application.agents.scheme_advisor_graph import SchemeAdvisorGraph
from application.agents.orchestrator_graph import OrchestratorGraph
from langgraph.graph.state import CompiledStateGraph


@dataclass
class Services:
        market_listing: MarketListingService
        llm_client: ILLMClient
        crop_advisor_graph: CompiledStateGraph
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

        llm_api_key = os.environ["ANTHROPIC_API_KEY"]
        claude_client = ClaudeClient(llm_api_key)

        langfuse = Langfuse(public_key=os.environ["LANGFUSE_PUBLIC_KEY"], secret_key=os.environ["LANGFUSE_SECRET_KEY"])
        llm_client = LangFuseClaudeClient(llm_client=claude_client, langfuse=langfuse, agent_name="crop_advisor")

        crop_advisor_graph = CropAdvisorGraph(llm_client=llm_client, weather_provider=StubWeatherProvider(), soil_moisture_provider=StubSoilMoistureProvider())
        
        crop_diagnosis_graph = CropDiagnosisGraph(llm_client=llm_client, weather_provider=StubWeatherProvider(), image_analyzer=StubImageAnalyser(), disease_corpus=StubDiseaseCorpus(), confirmation_repo=InMemoryConfirmationRepository())

        scheme_advisor_graph = SchemeAdvisorGraph(llm_client=llm_client, producer_repo=StubProducerRepository(), scheme_repo=StubSchemeRepository())

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
                        crop_advisor_graph=crop_advisor_graph.build(), 
                        crop_diagnosis_graph=crop_diagnosis_graph.build(), 
                        scheme_advisor_graph=scheme_advisor_graph.build(),
                        orchestrator_graph=orchestrator_graph.build(),
                        postgres_user_repo=postgres_user_repo,
                        postgres_conversation_repo=postgres_conversation_repo)
