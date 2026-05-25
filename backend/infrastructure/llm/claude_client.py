import anthropic
from typing import Iterator

class ClaudeClient:

    def __init__(self, api_key):
        self._llm_client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, messages: list) -> str:
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        user_messages = [m for m in messages if m["role"] != "system"]
        kwargs = {"model": "claude-haiku-4-5-20251001", "max_tokens": 1024, "messages": user_messages}
        if system:
            kwargs["system"] = system
        response = self._llm_client.messages.create(**kwargs)
        return response.content[0].text

    def stream(self, messages: list) -> Iterator[str]: 
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        user_messages = [m for m in messages if m["role"] != "system"]
        kwargs = {"model": "claude-haiku-4-5-20251001", "max_tokens": 1024, "messages": user_messages}
        if system:
            kwargs["system"] = system
            
        with self._llm_client.messages.stream(**kwargs) as s:
                for chunk in s.text_stream:
                    yield chunk
     