from domain.scheme_match import SchemeMatch
from domain.exceptions import InvalidConfidenceRangeError, EmptyReasonError
import pytest

class TestSchemeMatch:

    def test_scheme_match_defaults_to_empty_list(self):
        scheme_match = SchemeMatch("Good scheme",
                                   True, 
                                   "Your crop will qualify",
                                   0.95)
        
        assert len(scheme_match.missing_criteria) == 0
    
    def test_scheme_match_returns_values(self):
        scheme_match = SchemeMatch("Good scheme",
                                   True, 
                                   "Your crop will qualify",
                                   0.95,
                                   ["test1", "test2"])
        
        assert len(scheme_match.missing_criteria) == 2

    def test_scheme_match_raises_invalid_confidence_range_error(self):
        with pytest.raises(InvalidConfidenceRangeError):
            SchemeMatch("Good scheme",
                                   True, 
                                   "Your crop will qualify",
                                   1.95)
    
    def test_scheme_match_raises_empty_reason_error(self):
        with pytest.raises(EmptyReasonError):
            SchemeMatch("Good scheme",
                        True, 
                        "",
                        0.95)
            