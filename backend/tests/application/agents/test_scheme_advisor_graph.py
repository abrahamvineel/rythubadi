from tests.fakes.fake_llm_client import FakeLLMClient
from tests.fakes.in_memory_scheme_repository import InMemorySchemeRepository
from tests.fakes.in_memory_producer_repository import InMemoryProducerRepository
from application.agents.scheme_advisor_graph import SchemeAdvisorGraph
from application.agents.scheme_advisor_state import SchemeAdvisorState
from domain.regional_context import RegionalContext
from domain.language import Language
import uuid

class TestSchemeAdvisorGraph:   

    def test_scheme_advisor_returns_llm_response(self):
        scheme_advisor = SchemeAdvisorState(
                            producer_id=uuid.uuid4(),
                            region=RegionalContext("Andhra Pradesh"),
                            language=Language.EN,
                            question="What schemes am I eligible for?",
                            farmer_profile=None,
                            scheme_chunks=None,
                            scheme_matches=None,
                            llm_response=None,
                            tools_called=[]
                        )
        llm_client = FakeLLMClient("You are eligible for first scheme")
        result = SchemeAdvisorGraph(llm_client, InMemoryProducerRepository(), InMemorySchemeRepository()).build().invoke(scheme_advisor)
        assert result["llm_response"] == "You are eligible for first scheme"

    def test_scheme_advisor_calls_all_tools(self):
        scheme_advisor = SchemeAdvisorState(
                            producer_id=uuid.uuid4(),
                            region=RegionalContext("Andhra Pradesh"),
                            language=Language.EN,
                            question="What schemes am I eligible for?",
                            farmer_profile=None,
                            scheme_chunks=None,
                            scheme_matches=None,
                            llm_response=None,
                            tools_called=[]
                        )
        llm_client = FakeLLMClient("You are eligible for first scheme")
        result = SchemeAdvisorGraph(llm_client, InMemoryProducerRepository(), InMemorySchemeRepository()).build().invoke(scheme_advisor)
        assert result["tools_called"] == ["fetch_profile", "scheme_chunks", "check_eligibility", "respond"]
