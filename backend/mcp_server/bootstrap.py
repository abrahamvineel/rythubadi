from dataclasses import dataclass
from infrastructure.stubs.stub_soil_moisture_provider import StubSoilMoistureProvider
from infrastructure.stubs.stub_weather_provider import StubWeatherProvider
from infrastructure.stubs.stub_scheme_repository import StubSchemeRepository
from infrastructure.stubs.stub_image_analyser import StubImageAnalyser
from infrastructure.stubs.stub_producer_repository import StubProducerRepository
from application.ports.i_weather_provider import IWeatherProvider
from application.ports.i_soil_moisture_provider import ISoilMoistureProvider
from application.ports.i_scheme_repository import ISchemeRepository
from application.ports.i_image_analyzer import IImageAnalyzer
from application.ports.i_producer_repository import IProducerRepository

@dataclass
class Services:
    soil_moisture_provider: ISoilMoistureProvider
    weather_provider: IWeatherProvider
    scheme_repository: ISchemeRepository
    image_analyzer: IImageAnalyzer
    producer_repository: IProducerRepository

def build_dependencies():

    return Services(
        soil_moisture_provider=StubSoilMoistureProvider(),
        weather_provider=StubWeatherProvider(),
        scheme_repository=StubSchemeRepository(),
        image_analyzer=StubImageAnalyser(),
        producer_repository=StubProducerRepository()
    )
