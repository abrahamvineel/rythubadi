from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from bootstrap import build_services
from fastapi import APIRouter, Depends
from domain.product_category import ProductCategory
from domain.perishability_level import PerishabilityLevel
from domain.product import Product
from uuid import UUID
from domain.listing_mode import ListingMode
from presentation.dependencies import get_current_user
router = APIRouter()

class CreateListingRequest(BaseModel):
    price: Decimal
    listing_mode: ListingMode
    category: ProductCategory
    perishability: PerishabilityLevel
    photo_url: Optional[str] = None


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
