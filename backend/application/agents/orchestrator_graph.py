from application.agents.crop_advisor_graph import CropAdvisorGraph
from application.agents.crop_diagnosis_graph import CropDiagnosisGraph
from application.agents.scheme_advisor_graph import SchemeAdvisorGraph
from application.agents.orchestrator_state import OrchestratorState
from application.agents.crop_advisor_agent import AgentState
from application.agents.crop_diagnosis_state import CropDiagnosisState
from application.agents.scheme_advisor_state import SchemeAdvisorState
from application.ports.i_llm_client import ILLMClient
from application.prompt_injection_guard import sanitise
from langgraph.graph import StateGraph, END

class OrchestratorGraph:

    def __init__(self,
                 llm_client: ILLMClient,
                 crop_advisor: CropAdvisorGraph, 
                 crop_diagnosis: CropDiagnosisGraph, 
                 scheme_advisor: SchemeAdvisorGraph):
        self.llm_client = llm_client
        self.crop_advisor_graph = crop_advisor.build()
        self.crop_diagnosis_graph = crop_diagnosis.build()
        self.scheme_advisor_graph = scheme_advisor.build()
    
    def _classify_node(self, state: OrchestratorState) -> OrchestratorState:
        if state["has_image"] and state["image_url"]:
           return {**state, "routed_to": "crop_diagnosis"}
        sanitise(state["farmer_message"])
        prompt = [
            {"role": "system", "content": "Classify the farmer's question. Reply with exactly one word: crop_advisor, crop_diagnosis, or scheme_advisor."},
            {"role": "user", "content": state["farmer_message"]}
        ]
        routed_to = self.llm_client.generate(prompt).strip().lower()
        return {**state, "routed_to": routed_to}
    
    def _run_crop_advisor_node(self, state: OrchestratorState):
        advisor_input = AgentState(
            farmer_question = state["farmer_message"],
            crop_type       = state["crop_type"],
            region          = state["region"],
            language        = state["language"],
            producer_id     = state["producer_id"],
            producer_type   = state["producer_type"],
            recommendation  = None,
            confidence      = None,
            weather_context = None,
            soil_moisture   = None,
            data_disclaimer = None,
            error_details   = None,
            tools_called    = [],
            lat             = state.get("lat"),
            lon             = state.get("lon"),
        )
        result = self.crop_advisor_graph.invoke(advisor_input)
        answer = result["recommendation"]
        return {**state, "specialist_response": answer}
    
    def _route(self, state: OrchestratorState) -> str:
        if state["routed_to"] in ("crop_advisor", "crop_diagnosis", "scheme_advisor"):
             return state["routed_to"]
        return "crop_advisor"
    
    def _run_crop_diagnosis_node(self, state: OrchestratorState):
        advisor_input = CropDiagnosisState(
                image_url        = state["image_url"],
                crop_type        = state["crop_type"],
                region           = state["region"],
                language         = state["language"],
                producer_id      = state["producer_id"],
                weather_context  = None,
                disease_candidate = None,
                corpus_matches   = None,
                llm_diagnosis    = None,
                confirmation_id  = None,
                pending_confirmation = False,
                tools_called     = [],
                lat              = state.get("lat"),
                lon              = state.get("lon"),
        )
        result = self.crop_diagnosis_graph.invoke(advisor_input)
        answer = result["llm_diagnosis"]
        return {**state, "specialist_response": answer}    
    
    def _run_scheme_advisor_node(self, state: OrchestratorState):
        advisor_input = SchemeAdvisorState(
            producer_id    = state["producer_id"],
            region         = state["region"],
            language       = state["language"],
            question       = state["farmer_message"],
            farmer_profile = None,
            scheme_chunks  = None,
            scheme_matches = None,
            llm_response   = None,
            tools_called   = []
        )
        result = self.scheme_advisor_graph.invoke(advisor_input)
        answer = result["llm_response"]
        return {**state, "specialist_response": answer}
    
    def build(self):
        graph = StateGraph(OrchestratorState)
        graph.add_node("classify", self._classify_node)
        graph.add_node("crop_advisor", self._run_crop_advisor_node)
        graph.add_node("crop_diagnosis", self._run_crop_diagnosis_node)
        graph.add_node("scheme_advisor", self._run_scheme_advisor_node)
        graph.set_entry_point("classify")
        graph.add_conditional_edges("classify", self._route, {
            "crop_advisor": "crop_advisor",
            "crop_diagnosis": "crop_diagnosis",
            "scheme_advisor": "scheme_advisor"
        })
        graph.add_edge("crop_advisor", END)
        graph.add_edge("crop_diagnosis", END)
        graph.add_edge("scheme_advisor", END)
        return graph.compile()
    