from fastapi import APIRouter, HTTPException, Depends
from presentation.schemas.create_location_request import CreateLocationRequest
from presentation.dependencies.auth import get_current_user_id
from domain.farm_location import FarmLocation
from domain.producer_type import ProducerType
from domain.exceptions import UnauthorisedOperationError
from bootstrap import build_services
from uuid import UUID, uuid4

router = APIRouter()


def _serialise(loc: FarmLocation) -> dict:
    return {
        "id": str(loc.id),
        "name": loc.name,
        "latitude": float(loc.latitude),
        "longitude": float(loc.longitude),
        "producer_types": [t.name for t in loc.producer_types],
    }


@router.get("/locations")
def get_locations(user_id: UUID = Depends(get_current_user_id)):
    locations = build_services().postgres_location_repo.find_by_producer(user_id)
    return [_serialise(loc) for loc in locations]


@router.post("/locations", status_code=201)
def create_location(
    request: CreateLocationRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        producer_types = frozenset(ProducerType[t] for t in request.producer_types)
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Invalid producer type: {e}")

    location = FarmLocation(
        id=uuid4(),
        producer_id=user_id,
        name=request.name,
        latitude=request.latitude,
        longitude=request.longitude,
        producer_types=producer_types,
    )
    build_services().postgres_location_repo.save(location)
    return _serialise(location)


@router.delete("/locations/{location_id}", status_code=204)
def delete_location(
    location_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        build_services().postgres_location_repo.delete(location_id, user_id)
    except UnauthorisedOperationError:
        raise HTTPException(status_code=404, detail="Location not found")
