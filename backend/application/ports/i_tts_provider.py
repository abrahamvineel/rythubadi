from typing import Protocol
from domain.language import Language

class ITTSProvider(Protocol):

    def synthesise(self, text: str, language: Language) -> bytes: ...
