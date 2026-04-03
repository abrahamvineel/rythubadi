
INJECTION_PATTERNS = ["ignore previous instructions", "you are now", "disregard", "forget your instructions"]

class PromptInjectionDetectedError(Exception):
    """Raise exception when the prompt is injected by attacker"""
    def __init__(self, pattern: str):
        super().__init__(pattern)
        self.pattern = pattern

def sanitise(text: str) -> str:
    for pattern in INJECTION_PATTERNS:
        if pattern.lower() in text.lower():
            raise PromptInjectionDetectedError(pattern)
    return text
