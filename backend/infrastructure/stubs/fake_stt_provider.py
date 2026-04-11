
class FakeSTTProvider:

    def transcribe(self, audio_bytes: bytes) -> str:
        return "test transcript"
    