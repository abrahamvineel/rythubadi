from domain.scheme_chunk import SchemeChunk
from domain.exceptions import InvalidSimilarityScoreRangeError, EmptyContentError, EmptyCountryError
import pytest 

class TestSchemeChunk:

    def test_scheme_chunk_success(self):
        scheme_chunk = SchemeChunk("Farming scheme",
                                   "Good scheme",
                                   "No name",
                                   "No province",
                                   "https://no_name/farming/scheme",
                                   0.95)
        assert scheme_chunk.scheme_name == "Farming scheme"
        assert scheme_chunk.content == "Good scheme"

    def test_scheme_raises_error_on_invalid_similarty_score(self):
        with pytest.raises(InvalidSimilarityScoreRangeError):
            SchemeChunk("Farming scheme",
                        "Good scheme",
                        "No name",
                        "No province",
                        "https://no_name/farming/scheme",
                        1.95)
            
    def test_scheme_raises_error_on_empty_content(self):
        with pytest.raises(EmptyContentError):
            SchemeChunk("Farming scheme",
                        "",
                        "No name",
                        "No province",
                        "https://no_name/farming/scheme",
                        0.95)
            
    def test_scheme_raises_error_on_empty_country(self):
        with pytest.raises(EmptyCountryError):
            SchemeChunk("Farming scheme",
                        "Good scheme",
                        "",
                        "No province",
                        "https://no_name/farming/scheme",
                        0.95)
            
        
        
