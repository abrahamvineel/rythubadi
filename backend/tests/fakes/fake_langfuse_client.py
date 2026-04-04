from tests.fakes.fake_generation import FakeGeneration

class FakeLangFuseClient:

    def __init__(self):
        self.recorded_input = ""
    
    def generation(self, name: str, input: str, model: str) -> FakeGeneration:
        self.recorded_input = input
        return FakeGeneration()
