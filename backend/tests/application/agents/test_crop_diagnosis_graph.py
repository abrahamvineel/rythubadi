import uuid
from domain.language import Language
from tests.fakes.fake_confirmation_repository import FakeConfirmationRepository
from tests.fakes.fake_disease_corpus import FakeDiseaseCorpus
from tests.fakes.fake_image_analyser import FakeImageAnalyser
from tests.fakes.fake_weather_provider import FakeWeatherProvider
from tests.fakes.fake_llm_client import FakeLLMClient
from domain.human_loop.confirmable_action import ConfirmableAction
from application.agents.crop_diagnosis_state import CropDiagnosisState
from application.agents.crop_diagnosis_graph import CropDiagnosisGraph
from domain.weather_context import WeatherContext
from domain.data_precision import DataPrecision
from domain.regional_context import RegionalContext

class TestCropDiagnosisGraph:
    def test_diagnosis_saves_pending_confirmation(self):
        diagnosis_state = CropDiagnosisState(image_url="s3://image.jpg",
                                             crop_type="paddy", 
                                             region=RegionalContext("Andhra Pradesh", "IN"),
                                             language=Language.EN,
                                             producer_id=uuid.uuid4(),
                                             weather_context=None,
                                            disease_candidate=None,
                                            corpus_matches=None,
                                            llm_diagnosis=None,
                                            confirmation_id=None,
                                            pending_confirmation=False,
                                            tools_called=[],
                                            lat=None,
                                            lon=None)
        
        fake_image_analyser = FakeImageAnalyser("s3://image.jpg")
        fake_disease_corpus = FakeDiseaseCorpus(["image1", "image2"])
        fake_weather_provider = FakeWeatherProvider(WeatherContext(23.0, 23.0, 18.0, None, None, 10.9, None, None, 78.3, DataPrecision.DISTRICT))
        fake_llm_client = FakeLLMClient("Likely blast fungus disease")
        fake_confirmation_repository = FakeConfirmationRepository()

        crop_diagnosis_graph = CropDiagnosisGraph(fake_llm_client, fake_weather_provider, fake_image_analyser, fake_disease_corpus, fake_confirmation_repository)
        result = crop_diagnosis_graph.build().invoke(diagnosis_state)
        saved = list(fake_confirmation_repository.store.values())[0]

        assert len(fake_confirmation_repository.store) == 1
        assert saved.action == ConfirmableAction.CROP_DIAGNOSIS

    def test_diagnosis_returns_pending_true(self):
        diagnosis_state = CropDiagnosisState(image_url="s3://image.jpg",
                                         crop_type="paddy", 
                                         region=RegionalContext("Andhra Pradesh", "IN"),
                                         language=Language.EN,
                                         producer_id=uuid.uuid4(),
                                         weather_context=None,
                                        disease_candidate=None,
                                        corpus_matches=None,
                                        llm_diagnosis=None,
                                        confirmation_id=None,
                                        pending_confirmation=False,
                                        tools_called=[])
        
        fake_image_analyser = FakeImageAnalyser("s3://image.jpg")
        fake_disease_corpus = FakeDiseaseCorpus(["image1", "image2"])
        fake_weather_provider = FakeWeatherProvider(WeatherContext(23.0, 23.0, 18.0, None, None, 10.9, None, None, 78.3, DataPrecision.DISTRICT))
        fake_llm_client = FakeLLMClient("Likely blast fungus disease")
        fake_confirmation_repository = FakeConfirmationRepository()

        crop_diagnosis_graph = CropDiagnosisGraph(fake_llm_client, fake_weather_provider, fake_image_analyser, fake_disease_corpus, fake_confirmation_repository)
        result = crop_diagnosis_graph.build().invoke(diagnosis_state)

        assert len(fake_confirmation_repository.store) == 1
        assert result["pending_confirmation"] == True
        assert result["confirmation_id"] is not None
