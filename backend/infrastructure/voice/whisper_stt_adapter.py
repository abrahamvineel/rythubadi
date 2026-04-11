import io
from application.prompt_injection_guard import sanitise
from openai import OpenAI

class WhisperSTTAdapter:

    def __init__(self, client: OpenAI):
        self._client = client
    
    def transcribe(self, audio_bytes: bytes) -> str:
        buffer = io.BytesIO(audio_bytes)
        buffer.name = "audio.wav"
        result = self._client.audio.transcriptions.create(model="whisper-1", file=buffer)
        transcript = result.text
        return sanitise(transcript)
