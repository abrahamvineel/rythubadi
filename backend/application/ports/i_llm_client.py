from typing import Protocol

class ILLMClient(Protocol):
    
    def generate(self, messages: list) -> str: ...
    