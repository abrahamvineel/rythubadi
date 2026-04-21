from tests.fakes.in_memory_scheme_repository import InMemorySchemeRepository
from domain.regional_context import RegionalContext

class TestInMemorySchemeRepository:

    def test_search_returns_top_k_schemes(self):
        repo = InMemorySchemeRepository().search("test query", RegionalContext("Andhra Pradesh", "IN"), 2)
        
        assert len(repo) == 2