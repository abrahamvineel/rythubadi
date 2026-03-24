from domain.listing_mode import ListingMode
from domain.exceptions import InvalidPriceError, InvalidListingModeError
from domain.product import Product
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class MarketListing:
    listing_id: UUID
    listing_mode: ListingMode
    price: Decimal
    product: Product
    created_at: datetime
    producer_id: UUID
    is_active: bool

    def __post_init__(self):
        if not isinstance(self.listing_mode, ListingMode):
            raise InvalidListingModeError("Listing mode is invalid")
        elif (self.price <= 0 and (self.listing_mode in (ListingMode.SELL, ListingMode.BOTH))) or (self.price != 0 and self.listing_mode == ListingMode.DONATE):
            raise InvalidPriceError("Price cannot be less than or equal to zero in sell mode")
    
    def should_convert_to_donation(self, current_time: datetime) -> bool:
        expiry_at = self.created_at + self.product.perishability.to_timedelta()
        if current_time >= expiry_at:
            return True
        return False
