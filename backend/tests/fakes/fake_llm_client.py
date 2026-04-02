
class FakeLLMClient:

    def __init__(self, response):
        self.response = response
        self.input = ""

    def generate(self, input: str) -> str:
        self.input = input
        return self.response