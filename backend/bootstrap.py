from application.services.market_listing_service import MarketListingService
from backend.infrastructure.postgres_market_listing_repository import SupabaseMarketListingRepository

def build_services():
        repo = SupabaseMarketListingRepository(None)
        return MarketListingService(repo)

