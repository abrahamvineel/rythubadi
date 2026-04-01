
class FakeLLMClient:

    def __init__(self, response):
        self.response = response

    def generate(self, input: str) -> str:
        return self.response