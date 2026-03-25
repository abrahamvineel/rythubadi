from domain.listing_mode import ListingMode
from domain.market_listing import MarketListing
from domain.exceptions import InvalidPriceError, InvalidListingModeError, InvalidPhotoUrlError
from domain.product_category import ProductCategory
from domain.producer_profile import ProducerProfile
from domain.producer_type import ProducerType
from domain.perishability_level import PerishabilityLevel
from domain.product import Product
import uuid
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

class TestMarketListing:
    
    def test_create_market_listing_success(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = Decimal('0.1')
        created_at = datetime.now()
        profile = ProducerProfile(uuid.uuid4(), frozenset({ProducerType.FARMER}), "farmer1")
        market_listing = MarketListing(listing_id, listing_mode, price, product, created_at, profile.producer_id, True, None)

        assert market_listing.listing_id == listing_id
        assert market_listing.listing_mode == ListingMode.BOTH
        assert market_listing.price == price
        assert market_listing.product == product
        assert market_listing.created_at == created_at
        assert market_listing.producer_id == profile.producer_id
        
    def test_sell_price_less_than_or_equal_to_zero(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.SELL
        price = Decimal('0.0')
        created_at = datetime.now()
        
        with pytest.raises(InvalidPriceError):
            MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)

    def test_both_mode_price_zero_raises_invalid_price_error (self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = Decimal('0.0')
        created_at = datetime.now()
        
        with pytest.raises(InvalidPriceError):
            MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)
        

    def test_invalid_listing_mode(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = "INVALID"
        price = Decimal('0.0')
        created_at = datetime.now()
        
        with pytest.raises(InvalidListingModeError):
            MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)
               
    def test_should_convert_to_donation_success(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = Decimal('0.1')
        created_at = datetime.now()
        market_listing = MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)
        
        assert market_listing.should_convert_to_donation(created_at + timedelta(hours=7)) == True

               
    def test_should_convert_to_donation_before_threshold(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.BOTH
        price = Decimal('0.1')
        created_at = datetime.now()
        market_listing = MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)
        
        assert market_listing.should_convert_to_donation(created_at + timedelta(hours=0)) == False

    def test_donate_mode_price_not_zero_raises_invalid_price_error(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.DONATE
        price = Decimal('10.0')
        created_at = datetime.now()
        
        with pytest.raises(InvalidPriceError):
            MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)
    
    def test_donate_mode_price_zero_success(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.DONATE
        price = Decimal('0.0')
        created_at = datetime.now()
        MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, None)
    
    def test_add_photo_on_market_list(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.DONATE
        price = Decimal('0.0')
        created_at = datetime.now()
        photo_url = "aws.s3.market_list.photo1.jpg"
        MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, photo_url)
    
    def test_invalid_photo_url_on_market_list(self):
        product = Product(ProductCategory.CHEESE, PerishabilityLevel.CRITICAL)
        listing_id = uuid.uuid4()
        listing_mode = ListingMode.DONATE
        price = Decimal('0.0')
        created_at = datetime.now()
        with pytest.raises(InvalidPhotoUrlError):
            MarketListing(listing_id, listing_mode, price, product, created_at, uuid.uuid4(), True, "")
    