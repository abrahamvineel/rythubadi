from domain.regional_context import RegionalContext
from domain.scheme_chunk import SchemeChunk

class StubSchemeRepository:

    def search(self, query: str, regional_context: RegionalContext, top_k: int) -> list[SchemeChunk]:
        return [
                SchemeChunk("Farming scheme1",
                                   "Good scheme",
                                   "No name",
                                   "No province",
                                   "https://no_name/farming/scheme",
                                   0.95),
                SchemeChunk("Farming scheme2",
                                   "Good scheme",
                                   "No name",
                                   "No province",
                                   "https://no_name/farming/scheme",
                                   0.95)
        ]
    