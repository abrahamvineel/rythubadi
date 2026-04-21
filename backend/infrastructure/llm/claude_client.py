import anthropic

class ClaudeClient:

    def __init__(self, api_key):
        self._api_key = api_key
    
    def generate(self, messages: list) -> str:
        client = anthropic.Anthropic(api_key=self._api_key)
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        user_messages = [m for m in messages if m["role"] != "system"]
        kwargs = {"model": "claude-haiku-4-5-20251001", "max_tokens": 1024, "messages": user_messages}
        if system:
            kwargs["system"] = system
        response = client.messages.create(**kwargs)
        return response.content[0].text
