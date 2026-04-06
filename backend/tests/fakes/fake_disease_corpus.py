
class FakeDiseaseCorpus:

    def __init__(self, response: list[str]):
        self.response = response

    def search(self, query: str) -> list[str]:
        return self.response
    