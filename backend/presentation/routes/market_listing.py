from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from bootstrap import build_services
from fastapi import APIRouter, Depends, Query, HTTPException
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.product import Product
from uuid import UUID
from domain.listing_mode import ListingMode
from presentation.dependencies import get_current_user
from datetime import datetime
import base64
import json
from domain.exceptions import ListingNotFoundError

router = APIRouter()

class CreateListingRequest(BaseModel):
    price: Decimal
    listing_mode: ListingMode
    category: ProductCategory
    perishability: PerishabilityLevel
    photo_url: Optional[str] = None

class ListingItem(BaseModel):
    listing_id: UUID
    listing_mode: str
    product_category: str
    perishability_level: str
    price: Decimal
    created_at: datetime
    producer_id: UUID
    is_active: bool
    photo_url: Optional[str]

class ListingResponse(BaseModel):
    listings: list[ListingItem]
    next_cursor: Optional[str]


def get_market_listing_service():
    return build_services()

@router.post("/listings", status_code=201)
def create_listing(request: CreateListingRequest,
                   claims: dict = Depends(get_current_user),
                   service = Depends(get_market_listing_service)):
    product = Product(request.category,
                request.perishability)
    
    service.create_listing(request.listing_mode,
                           request.price,
                           product,
                           UUID(claims["sub"]),
                           request.photo_url)
    return {"status": "created"}

@router.get("/listings", status_code=200)
def get_listings(cursor: Optional[str] = Query(default=None), 
                 limit: int = Query(default=20, ge=1, le=50),
                 claims: dict = Depends(get_current_user),
                 service = Depends(get_market_listing_service)):
    created_at = None
    listing_id = None

    if cursor is not None:
        try:
            decoded = base64.b64decode(cursor).decode("utf-8")
            data = json.loads(decoded)
            created_at = datetime.fromisoformat(data["created_at"])
            listing_id = UUID(data["listing_id"])
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid cursor")

    active_listings = service.get_active_listings_for_cursor(limit, created_at, listing_id)

    items = [ListingItem(
        listing_id=l.listing_id,
        listing_mode=l.listing_mode.name,
        product_category=l.product.category.name,
        perishability_level=l.product.perishability.name,
        price=l.price,
        created_at=l.created_at,
        producer_id=l.producer_id,
        is_active=l.is_active,
        photo_url=l.photo_url
    ) for l in active_listings]

    next_cursor = None
    if len(active_listings) == limit:
        last = active_listings[-1]
        next_cursor = base64.b64encode(json.dumps({
            "created_at": last.created_at.isoformat(), 
            "listing_id": str(last.listing_id)
        }).encode()).decode("utf-8")

    return ListingResponse(listings=items, next_cursor=next_cursor)

@router.get("/listings/{listing_id}", status_code=200)
def get_listing(listing_id: UUID,
                claims: dict = Depends(get_current_user),
                service = Depends(get_market_listing_service)):
    try:
        listing = service.get_listing_by_id(listing_id)
        return ListingItem(
            listing_id=listing.listing_id,
            listing_mode=listing.listing_mode.name,
            product_category=listing.product.category.name,
            perishability_level=listing.product.perishability.name,
            price=listing.price,
            created_at=listing.created_at,
            producer_id=listing.producer_id,
            is_active=listing.is_active,
            photo_url=listing.photo_url
        )
    except ListingNotFoundError:
        raise HTTPException(status_code=404, detail="Listing not found in database")



