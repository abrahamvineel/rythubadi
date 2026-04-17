from typing import Protocol, Optional
from domain.user import User

class IUserRepository(Protocol):

    def save(self, user: User) -> None: ...

    def find_by_email(self, email: str) -> Optional[User]: ...

    def find_by_phone_number(self, phone: str) -> Optional[User]: ...
