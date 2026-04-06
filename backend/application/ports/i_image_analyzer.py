from typing import Protocol

class IImageAnalyzer(Protocol):

    def analyse_image(self, image_url: str) -> str: ...