from typing import Protocol

class IImageStorage(Protocol):
    def upload(self, data: bytes, filename: str, content_type: str) -> str: ...
    