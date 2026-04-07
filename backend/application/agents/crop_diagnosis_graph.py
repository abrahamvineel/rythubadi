from application.agents.crop_diagnosis_state import CropDiagnosisState
from application.ports.i_llm_client import ILLMClient
from application.ports.i_weather_provider import IWeatherProvider
from application.ports.i_image_analyzer import IImageAnalyzer
from application.ports.i_disease_corpus import IDiseaseCorpus
from application.ports.i_confirmation_repository import IConfirmationRepository
from datetime import datetime, timezone, timedelta
from domain.human_loop.human_confirmation import HumanConfirmation
from domain.human_loop.confirmable_action import ConfirmableAction
from langgraph.graph import StateGraph, END
import uuid

class CropDiagnosisGraph:

    def __init__(self, 
                 llm_client: ILLMClient,
                 weather_provider: IWeatherProvider,
                 image_analyzer: IImageAnalyzer,
                 disease_corpus: IDiseaseCorpus,
                 confirmation_repo: IConfirmationRepository):
        self.llm_client = llm_client
        self.weather_provider = weather_provider
        self.image_analyzer = image_analyzer
        self.disease_corpus = disease_corpus
        self.confirmation_repo = confirmation_repo

    def _fetch_weather_node(self, state: CropDiagnosisState) -> CropDiagnosisState:
        result = self.weather_provider.get_weather(state["region"].province_state)
        return {**state, "weather_context": result, "tools_called": state["tools_called"] + ["weather"]}
    
    def _analyse_image_node(self, state: CropDiagnosisState) -> CropDiagnosisState:
        result = self.image_analyzer.analyse_image(state["image_url"])
        return {**state, "disease_candidate": result, "tools_called": state["tools_called"] + ["image"]}

    def _search_corpus_node(self, state: CropDiagnosisState) -> CropDiagnosisState:
        result = self.disease_corpus.search(state["disease_candidate"])
        return {**state, "corpus_matches": result, "tools_called": state["tools_called"] + ["corpus_search"]}

    def _diagnose_node(self, state: CropDiagnosisState) -> CropDiagnosisState:
        response = self.llm_client.generate(self._build_prompt(state))
        confirmation = self._get_confirmation(state)
        self.confirmation_repo.save(confirmation=confirmation)
        return {**state, "llm_diagnosis":response, "confirmation_id": confirmation.confirmation_id, "pending_confirmation": True}

    def _build_prompt(self, state: CropDiagnosisState) -> list:
        weather_info = f"Temperature: {state['weather_context'].temperature}°C" if state["weather_context"] else "Weather unavailable." 
        system_message =  f"You are an expert in analysing crop image to detect diseases." \
                f"analyse the image {state['image_url']} thoroughly" \
                + weather_info + f"the possible disease candidate is {state['corpus_matches']}" \
                f"Image analysis identified: {state['disease_candidate']}. " \
                f"Supporting corpus matches: {', '.join(state['corpus_matches'] or [])}."
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Diagnose the crop disease from the image and context above."}
        ]

    def _get_confirmation(self, state: CropDiagnosisState) -> HumanConfirmation:
        return HumanConfirmation(
            confirmation_id=uuid.uuid4(),
            action=ConfirmableAction.CROP_DIAGNOSIS,
            producer_id=state["producer_id"],
            summary=f"Crop diagnosis for {state['crop_type']} in {state['region'].province_state}",
            consequences="Treatment advice will be sent to the farmer upon confirmation.",
            expires_at=datetime.now(timezone.utc) + timedelta(hours=4)
        )

    def build(self):
        graph = StateGraph(CropDiagnosisState)
        graph.add_node("fetch_weather", self._fetch_weather_node)
        graph.add_node("analyse_image", self._analyse_image_node)
        graph.add_node("search_corpus", self._search_corpus_node)
        graph.add_node("diagnose", self._diagnose_node)
        graph.set_entry_point("fetch_weather")
        graph.add_edge("fetch_weather", "analyse_image")
        graph.add_edge("analyse_image", "search_corpus")
        graph.add_edge("search_corpus", "diagnose")
        graph.add_edge("diagnose", END)
        return graph.compile()
    