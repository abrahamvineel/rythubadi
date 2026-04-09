from application.agents.crop_advisor_graph import CropAdvisorGraph
from application.agents.crop_diagnosis_graph import CropDiagnosisGraph
from application.agents.scheme_advisor_graph import SchemeAdvisorGraph
from application.agents.orchestrator_state import OrchestratorState
from application.ports.i_llm_client import ILLMClient

class OrchestratorGraph:

    def __init__(self,
                 llm_client: ILLMClient,
                 crop_advisor: CropAdvisorGraph, 
                 crop_diagnosis: CropDiagnosisGraph, 
                 scheme_advisor: SchemeAdvisorGraph):
        self.llm_client = llm_client
        self.crop_advisor = crop_advisor.build()
        self.crop_diagnosis = crop_diagnosis.build()
        self.scheme_advisor = scheme_advisor.build()
    
    def _classify_node(self, state: OrchestratorState) -> OrchestratorState:
        if state["has_image"]:
           return {**state, "routed_to": "crop_diagnosis"}
        
