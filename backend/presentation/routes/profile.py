from fastapi import APIRouter, HTTPException, Depends
from presentation.schemas.add_producer_types_request import AddProducerTypesRequest
from presentation.dependencies.auth import get_current_user_id
from domain.producer_type import ProducerType
from bootstrap import build_services
from uuid import UUID

router = APIRouter()


@router.get("/profile")
def get_profile(user_id: UUID = Depends(get_current_user_id)):
    profile = build_services().postgres_producer_repo.find_by_id(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"producer_types": [t.name for t in profile.producer_types]}


@router.patch("/profile/types")
def add_producer_types(
    request: AddProducerTypesRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        new_types = frozenset(ProducerType[t] for t in request.producer_types)
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Invalid producer type: {e}")

    updated = build_services().postgres_producer_repo.add_types(user_id, new_types)
    return {"producer_types": [t.name for t in updated.producer_types]}
