
class FakeLLMClient:

    def __init__(self, response):
        self.response = response
        self.input = ""

    def generate(self, messages: list) -> str:
        self.input = messages
        return self.response