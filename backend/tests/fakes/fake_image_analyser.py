
class FakeImageAnalyser:

    def __init__(self, response:str):
        self.response = response

    def analyse_image(self, image_url: str) -> str:
        return self.response
    