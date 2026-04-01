from typing import Protocol

class ILLMClient(Protocol):
    
    def generate(self, input: str) -> str: ...
    