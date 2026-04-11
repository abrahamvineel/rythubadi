from domain.language import Language

class FakeTTSProvider:

    def synthesise(self, text: str, language: Language) -> bytes:
        return b""
    