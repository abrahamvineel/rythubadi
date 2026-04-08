from application.ports.i_llm_client import ILLMClient
from application.ports.i_scheme_repository import ISchemeRepository
from application.ports.i_producer_repository import IProducerRepository
from application.agents.scheme_advisor_state import SchemeAdvisorState
from domain.scheme_chunk import SchemeChunk
from domain.producer_profile import ProducerProfile

class SchemeAdvisorGraph:

    def __init__(self, llm_client: ILLMClient, producer_repo: IProducerRepository, scheme_repo: ISchemeRepository):
        self.llm_client = llm_client
        self.producer_repo = producer_repo
        self.scheme_repo = scheme_repo

    def _fetch_profile_node(self, state: SchemeAdvisorState) -> SchemeAdvisorState:
        farmer_profile = self.producer_repo.find_by_id(state["producer_id"])
        return {**state, "farmer_profile": farmer_profile, "tools_called": state["tools_called"] + ["fetch_profile"]}

    def _search_schemes_node(self, state: SchemeAdvisorState) -> SchemeAdvisorState:
        profile = state["farmer_profile"]
        query = f"schemes for {profile.producer_types} farmer in {state['region'].province_state}"
        result = self.scheme_repo.search(query, state["region"], top_k=5)
        return {**state, "scheme_chunks": result, "tools_called": state["tools_called"] + ["scheme_chunks"]}
    
    def _check_eligibility_node(self, state: SchemeAdvisorState) -> SchemeAdvisorState:
        prompt = self._build_prompt(state["scheme_chunks"], state["farmer_profile"])
        result = self.llm_client.generate()

    def _build_prompt(self, scheme_chunks: SchemeChunk, farmer_profile: ProducerProfile) -> list[str]:
        return [{
            "role": ""
        }]