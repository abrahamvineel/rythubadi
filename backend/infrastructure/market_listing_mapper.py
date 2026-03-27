from uuid import UUID
from domain.product import Product
from decimal import Decimal
from datetime import datetime
from domain.listing_mode import ListingMode
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.market_listing import MarketListing

def row_to_domain(row: dict) -> MarketListing:
    listing_id = UUID(row["listing_id"])
    listing_mode = ListingMode[row["listing_mode"]]
    product = Product(ProductCategory[row["product_category"]], PerishabilityLevel[row["perishability_level"]])
    price = Decimal(row["price"])
    created_at = datetime.fromisoformat(row["created_at"])
    producer_id = UUID(row["producer_id"])
    is_active = row["is_active"]
    photo_url = row["photo_url"]

    return MarketListing(listing_id, listing_mode, price, product, created_at, producer_id, is_active, photo_url)

def domain_to_row(listing: MarketListing) -> dict:
    return {
        "listing_id": listing.listing_id,
        "listing_mode": listing.listing_mode.name,
        "product_category": listing.product.category.name,
        "perishability_level": listing.product.perishability.name,
        "price": listing.price,
        "created_at": listing.created_at,
        "producer_id": listing.producer_id,
        "is_active": listing.is_active,
        "photo_url": listing.photo_url
    }
