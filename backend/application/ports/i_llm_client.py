from typing import Protocol, Iterator

class ILLMClient(Protocol):
    
    def generate(self, messages: list) -> str: ...
    
    def stream(self, messages: list) -> Iterator[str]: ...
        