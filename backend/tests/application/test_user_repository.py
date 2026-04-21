from domain.user import User
from domain.language import Language
from domain.regional_context import RegionalContext
from tests.fakes.in_memory_user_repository import InMemoryUserRepository
import uuid

def _make_user(email=None, phone_number=None) -> User:
    return User(
        id=uuid.uuid4(),
        email=email,
        phone_number=phone_number,
        name="abc",
        password_hash="hashed_password",
        language=Language.EN,
        province_state=RegionalContext("Andhra Pradesh", "IN"),
    )

class TestUserRepository:

    def test_save_and_find_by_email(self):
        repo = InMemoryUserRepository()
        user = _make_user(email="abc@gmail.com", phone_number="0000000000")
        repo.save(user)

        found = repo.find_by_email("abc@gmail.com")

        assert found.email == "abc@gmail.com"
        assert found.phone_number == "0000000000"

    def test_find_by_phone_number(self):
        repo = InMemoryUserRepository()
        user = _make_user(phone_number="0000000000")
        repo.save(user)

        found = repo.find_by_phone_number("0000000000")

        assert found.phone_number == "0000000000"
        assert found.email is None

    def test_find_by_email_returns_none_when_not_found(self):
        repo = InMemoryUserRepository()

        found = repo.find_by_email("notexist@gmail.com")

        assert found is None
