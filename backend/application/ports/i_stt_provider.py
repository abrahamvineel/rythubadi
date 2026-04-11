from typing import Protocol

class ISTTProvider(Protocol):

    def transcribe(self, audio_bytes: bytes) -> str: ...
