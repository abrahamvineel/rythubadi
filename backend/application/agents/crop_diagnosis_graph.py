from application.agents.crop_diagnosis_state import CropDiagnosisState
from application.ports.i_llm_client import ILLMClient
from application.ports.i_weather_provider import IWeatherProvider
from application.ports.i_image_analyzer import IImageAnalyzer
from application.ports.i_disease_corpus import IDiseaseCorpus
from application.ports.i_confirmation_repository import IConfirmationRepository

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
        result = self.llm_client.generate(result[""])

    def _build_prompt(self, state: CropDiagnosisState) -> str:
        return f"You are an expert in analysing crop image to detect diseases." \
                f"analyse the image {state["image_url"]} thoroughly" \
                f"current weather is {state["weather_context"].temperature}"\
                f"the possible disease candidate is {state["corpus_matches"]}"
    