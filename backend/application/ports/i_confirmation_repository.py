from domain.human_loop.human_confirmation import HumanConfirmation
from typing import Protocol

class IConfirmationRepository(Protocol):

    def save(self, confirmation: HumanConfirmation) -> None: ...
    