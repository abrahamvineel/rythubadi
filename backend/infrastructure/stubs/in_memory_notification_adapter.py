from uuid import UUID

class InMemoryNotificationAdapter:

    def __init__(self):
        self.sent: list[dict] = []

    def send(self, producer_id: UUID, message: str, language: str) -> None:
        self.sent.append({
            "producer_id": str(producer_id),
            "message": message,
            "language": language,
        })
        print(f"[NOTIFICATION] producer={producer_id} lang={language}\n{message}")
