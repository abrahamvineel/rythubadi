from domain.user import User
from tests.fakes.in_memory_user_repository import InMemoryUserRepository
import uuid
from datetime import datetime

class TestUserRepository:

    def test_save_and_find_by_email(self):
        repo = InMemoryUserRepository()
        user = User(uuid.uuid4(), "abc@gmail.com", "0000000000", 
                    "abc", "hashed_password", datetime.now())
        repo.save(user)

        found = repo.find_by_email("abc@gmail.com")
        
        assert found.email == "abc@gmail.com"
        assert found.phone_number == "0000000000"

    def test_find_by_phone_number(self):
        repo = InMemoryUserRepository()
        user = User(uuid.uuid4(), None, "0000000000",
                    "abc", "hashed_password", datetime.now())
        repo.save(user)

        found = repo.find_by_phone_number("0000000000")

        assert found.phone_number == "0000000000"
        assert found.email is None

    def test_find_by_email_returns_none_when_not_found(self):
        repo = InMemoryUserRepository()

        found = repo.find_by_email("notexist@gmail.com")

        assert found is None
