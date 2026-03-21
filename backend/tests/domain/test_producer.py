from domain.producer import ProducerProfile
from domain.producer_type import ProducerType
from domain.exceptions import UnauthorisedOperationError
import uuid
import pytest

class TestProducerProfile:
    
    def test_check_ownership_success(self):
        profile = ProducerProfile(uuid.uuid4(), ProducerType.FARMER, "farmer1")
        profile.check_ownership(profile.producer_id)

    def test_check_ownership_raises_error(self):
        profile = ProducerProfile(uuid.uuid4(), ProducerType.FARMER, "farmer1")
        attacker = ProducerProfile(uuid.uuid4(), ProducerType.FARMER, "farmer2")
        with pytest.raises(UnauthorisedOperationError):
            profile.check_ownership(attacker.producer_id)
