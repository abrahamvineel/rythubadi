from typing import Protocol

class IDiseaseCorpus(Protocol):

    def search(self, query: str) -> list[str]: ...
    