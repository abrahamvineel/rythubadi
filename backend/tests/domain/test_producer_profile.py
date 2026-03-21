from domain.producer_profile import ProducerProfile
from domain.producer_type import ProducerType
from domain.exceptions import UnauthorisedOperationError, NoProducerTypeError, InvalidProducerTypeError
import uuid
import pytest

class TestProducerProfile:
    
    def test_check_ownership_success(self):
        profile = ProducerProfile(uuid.uuid4(), frozenset({ProducerType.FARMER}), "farmer1")
        profile.check_ownership(profile.producer_id)

    def test_check_ownership_raises_error(self):
        profile = ProducerProfile(uuid.uuid4(), frozenset({ProducerType.FARMER}), "farmer1")
        attacker = ProducerProfile(uuid.uuid4(), frozenset({ProducerType.FARMER}), "farmer2")
        with pytest.raises(UnauthorisedOperationError):
            profile.check_ownership(attacker.producer_id)

    def test_producer_type_empty_frozen(self):
        with pytest.raises(NoProducerTypeError):
            ProducerProfile(uuid.uuid4(), frozenset({}), "farmer1")

    def test_invalid_producer_type(self):
                with pytest.raises(InvalidProducerTypeError):
                     ProducerProfile(uuid.uuid4(), frozenset({"INVALID_TYPE"}), "farmer1")
