from domain.listing_mode import ListingMode
from domain.market_listing import MarketListing
from domain.exceptions import InvalidPriceError, InvalidListingModeError
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.product import Product
import uuid
import pytest
from datetime import datetime, timedelta

class TestMarketListing:
    
    def test_create_market_listing_success(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = 0.1
        created_at = datetime.now()
        market_listing = MarketListing(listing_id, listing_mode, price, product, created_at)
    
        assert market_listing.listing_id == listing_id
        assert market_listing.listing_mode == ListingMode.BOTH
        assert market_listing.price == price
        assert market_listing.product == product
        assert market_listing.created_at == created_at
        

    def test_sell_price_less_than_or_equal_to_zero(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.SELL
        price = 0.0
        created_at = datetime.now()
        
        with pytest.raises(InvalidPriceError):
            MarketListing(listing_id, listing_mode, price, product, created_at)

    def test_both_mode_price_zero_raises_invalid_price_error (self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = 0.0
        created_at = datetime.now()
        
        with pytest.raises(InvalidPriceError):
            MarketListing(listing_id, listing_mode, price, product, created_at)
        

    def test_invalid_listing_mode(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = "INVALID"
        price = 0.0
        created_at = datetime.now()
        
        with pytest.raises(InvalidListingModeError):
            MarketListing(listing_id, listing_mode, price, product, created_at)
               
    def test_should_convert_to_donation_success(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = 0.1
        created_at = datetime.now()
        market_listing = MarketListing(listing_id, listing_mode, price, product, created_at)
        
        assert market_listing.should_convert_to_donation(created_at + timedelta(hours=7)) == True

               
    def test_should_convert_to_donation_before_threshold(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = 0.1
        created_at = datetime.now()
        market_listing = MarketListing(listing_id, listing_mode, price, product, created_at)
        
        assert market_listing.should_convert_to_donation(created_at + timedelta(hours=0)) == False


