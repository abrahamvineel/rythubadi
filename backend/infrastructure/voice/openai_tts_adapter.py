from openai import OpenAI
from domain.language import Language

class OpenAITTSAdapter:
    
    def __init__(self, client: OpenAI):
        self._client = client
    
    def synthesise(self, text: str, language: Language) -> bytes:
        result = self._client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
            response_format="mp3"
        )

        return result.read()
    