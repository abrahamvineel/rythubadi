from typing import Protocol
from domain.regional_context import RegionalContext
from domain.scheme_chunk import SchemeChunk

class ISchemeRepository(Protocol):

    def search(self, query: str, regional_context: RegionalContext, top_k: int) -> list[SchemeChunk]: ...
