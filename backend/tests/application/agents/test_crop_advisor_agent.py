from tests.fakes.fake_llm_client import FakeLLMClient
from domain.producer_type import ProducerType
from application.agents.crop_advisor_agent import AgentState, advise
from domain.regional_context import RegionalContext
import uuid

class TestCropAdvisorAgent:

    def test_generate_success(self):
        agent_state = AgentState(farmer_question="When should i water the crop?",
                                 recommendation=None, 
                                 producer_id=uuid.uuid4(), 
                                 producer_type=ProducerType.FARMER,
                                 crop_type="paddy field", 
                                 region=RegionalContext("Andhra Pradesh"), 
                                 error_details=None)
        llm_client = FakeLLMClient("Crop should be watered now.")               
        result = advise(agent_state, llm_client)
        assert result["recommendation"] == "Crop should be watered now."

    def test_generate_fallback_when_llm_returns_empty(self):
        agent_state = AgentState(farmer_question="When should i water the crop?",
                                 recommendation=None, 
                                 producer_id=uuid.uuid4(), 
                                 producer_type=ProducerType.FARMER,
                                 crop_type="paddy field", 
                                 region=RegionalContext("Andhra Pradesh"), 
                                 error_details=None)
        llm_client = FakeLLMClient("")               
        result = advise(agent_state, llm_client)
        assert result["recommendation"] == ("Unable to get recommendation right now, "
        " Based on your region and this time of season, here's what to consider while you wait: "
        "[general guidance]. You can also consult your local agricultural extension office")
        assert result["error_details"] == "LLM response is empty"
