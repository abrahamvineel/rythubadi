from application.ports.i_llm_client import ILLMClient
from application.ports.i_scheme_repository import ISchemeRepository
from application.ports.i_producer_repository import IProducerRepository
from application.agents.scheme_advisor_state import SchemeAdvisorState
from langgraph.graph import StateGraph, END

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
        prompt = self._build_eligibility_prompt(state["scheme_chunks"], state["farmer_profile"])
        result = self.llm_client.generate(prompt)
        return {**state, "scheme_matches": result, "tools_called": state["tools_called"] + ["check_eligibility"]}
    
    def _respond_node(self, state: SchemeAdvisorState) -> SchemeAdvisorState:
        prompt = self._build_response_prompt(state["scheme_matches"], state["language"])
        result = self.llm_client.generate(prompt)
        return {**state, "llm_response": result, "tools_called": state["tools_called"] + ["respond"]}
    
    def build(self):
        graph = StateGraph(SchemeAdvisorState)
        graph.add_node("fetch_profile", self._fetch_profile_node)
        graph.add_node("schemes_chunks", self._search_schemes_node)
        graph.add_node("check_eligibility", self._check_eligibility_node)
        graph.add_node("respond", self._respond_node)
        graph.set_entry_point("fetch_profile")
        graph.add_edge("fetch_profile", "schemes_chunks")
        graph.add_edge("schemes_chunks", "check_eligibility")
        graph.add_edge("check_eligibility", "respond")
        graph.add_edge("respond", END)
        return graph.compile()
    
    def _build_eligibility_prompt(self, scheme_chunks, farmer_profile) -> list[str]:
        chunks_text = "\n\n".join([
            f"Scheme: {chunk.scheme_name}\n{chunk.content}"
            for chunk in scheme_chunks
        ])
        system_message = (
            f"You are a government scheme eligibility advisor. "
            f"The farmer has producer types: {farmer_profile.producer_types}, "
            f"located in: {farmer_profile.name}. "  
            f"Here are the relevant scheme documents:\n\n{chunks_text}"
        )
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Which of these schemes is this farmer eligible for? For each scheme state: eligible (yes/no), reason, and confidence (0.0-1.0)."}
        ]
    
    def _build_response_prompt(self, scheme_matches, language):
        system_message = (
            f"You are a helpful agricultural advisor. "
            f"Here are the scheme eligibility results:\n\n{scheme_matches}"
            f"Respond in {language.value}."
        )

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Summarize which schemes this farmer qualifies for and what action they should take next."}
        ]
