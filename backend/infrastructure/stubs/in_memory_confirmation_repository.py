from domain.human_loop.human_confirmation import HumanConfirmation
from uuid import UUID

class InMemoryConfirmationRepository:

    def __init__(self):
        self.store: dict[UUID, HumanConfirmation] = {}

    def save(self, confirmation: HumanConfirmation) -> None:
        self.store[confirmation.confirmation_id] = confirmation
