from application.ports.i_market_listing_repository import IMarketListingRepository
from datetime import datetime
from domain.product import Product
from domain.listing_mode import ListingMode
from datetime import datetime
from decimal import Decimal
from domain.market_listing import MarketListing
from uuid import UUID, uuid4
from typing import Optional

class MarketListingService:
    
    def __init__(self, repo: IMarketListingRepository):
        self.repo = repo

    def create_listing(self, 
                       listing_mode: ListingMode,
                       price: Decimal,
                       product: Product,
                       producer_id: UUID,
                       photo_url: Optional[str]) -> None:
        
        listing = MarketListing(
            uuid4(), 
            listing_mode, 
            price,
            product,
            datetime.now(), 
            producer_id, 
            True,
            photo_url
        )        

        self.repo.save(listing)


    def run_donation_sweep(self, current_time: datetime) -> None:
            active_listings = self.repo.find_all_active()
            for active_listing in active_listings:
                        with self.repo.transaction(): 
                               if active_listing.should_convert_to_donation(current_time):
                                      self.repo.deactivate(active_listing.listing_id)
                                      listing = MarketListing(
                                                    uuid4(), 
                                                    ListingMode.DONATE, 
                                                    Decimal('0.0'),
                                                    active_listing.product,
                                                    current_time, 
                                                    active_listing.producer_id, 
                                                    True,
                                                    active_listing.photo_url
                                                )        

                                      self.repo.save(listing)

    def get_active_listings_for_cursor(self, limit: int, created_at: Optional[datetime], listing_id: Optional[UUID]):
           return self.repo.find_active(limit, created_at, listing_id)
