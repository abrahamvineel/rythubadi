from typing import Optional
from uuid import UUID
from domain.user import User


class InMemoryUserRepository:

    def __init__(self):
        self._store: dict[UUID, User] = {}

    def save(self, user: User) -> None:
        self._store[user.id] = user

    def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._store.values() if u.email == email), None)

    def find_by_phone_number(self, phone: str) -> Optional[User]:
        return next((u for u in self._store.values() if u.phone_number == phone), None)
