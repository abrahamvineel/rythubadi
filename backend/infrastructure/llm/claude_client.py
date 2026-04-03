import anthropic

class ClaudeClient:

    def __init__(self, api_key):
        self._api_key = api_key
    
    def generate(self, messages: list) -> str:
        client = anthropic.Anthropic(api_key=self._api_key)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=messages
        )
        return response.content[0].text
