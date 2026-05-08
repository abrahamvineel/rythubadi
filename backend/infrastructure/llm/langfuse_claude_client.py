from application.ports.i_llm_client import ILLMClient
import hashlib
from langfuse import observe, get_client
from typing import Iterator

class LangFuseClaudeClient:

    def __init__(self, llm_client: ILLMClient, agent_name: str):
        self._llm_client = llm_client
        self._agent_name = agent_name

    @observe(as_type="generation")
    def generate(self, messages: list) -> str:
        get_client().update_current_generation(
            name=self._agent_name,
            input=self._hash(messages),
            model="claude-haiku-4-5-20251001",
        )
        result = self._llm_client.generate(messages)
        get_client().update_current_generation(
            output=self._hash(result),
        )
        return result

    def _hash(self, value) -> str:
        return hashlib.sha256(str(value).encode()).hexdigest()
    
    @observe(as_type="generation")
    def stream(self, messages: list) -> Iterator[str]:
        get_client().update_current_generation(
            name=self._agent_name,
            input=self._hash(messages),
            model="claude-haiku-4-5-20251001",
        )
        chunks = []
        for chunk in self._llm_client.stream(messages):
            chunks.append(chunk)
            yield chunk
        full_response = "".join(chunks)
        get_client().update_current_generation(output=self._hash(full_response))
