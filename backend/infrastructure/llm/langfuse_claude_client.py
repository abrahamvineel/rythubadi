from application.ports.i_llm_client import ILLMClient
import time
import hashlib

class LangFuseClaudeClient:
    
    def __init__(self, llm_client: ILLMClient, langfuse, agent_name: str):
        self._llm_client = llm_client
        self._langfuse = langfuse

        self._agent_name = agent_name
    
    def generate(self, messages: list) -> str:
        start_time = time.time()
        sha256_of_messages = self._hash(messages)
        generation = self._langfuse.generation(name=self._agent_name, input=sha256_of_messages, model="claude-haiku-4-5-20251001")
        result = self._llm_client.generate(messages)
        end_time = time.time()
        generation.end(output=self._hash(result), latency=end_time-start_time)
        return result
    
    def _hash(self, response: str):
        return hashlib.sha256(str(response).encode()).hexdigest()