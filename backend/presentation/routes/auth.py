from fastapi import APIRouter, HTTPException
from presentation.schemas.register_request import RegisterRequest
from presentation.schemas.login_request import LoginRequest
from domain.user import User
from domain.language import Language
from domain.regional_context import RegionalContext
from domain.producer_profile import ProducerProfile
from domain.producer_type import ProducerType
from bootstrap import build_services
import uuid
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

router = APIRouter()

@router.post("/auth/register")
def register(request: RegisterRequest):
    jwt_secret = os.environ["JWT_SECRET"]
    services = build_services()

    existing = (
        services.postgres_user_repo.find_by_email(request.email)
        if request.email
        else services.postgres_user_repo.find_by_phone_number(request.phone_number)
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="Account already exists")

    try:
        producer_types = frozenset(ProducerType[t] for t in request.producer_types)
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Invalid producer type: {e}")

    hash_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
    user = User(
        id=uuid.uuid4(),
        email=request.email,
        phone_number=request.phone_number,
        name=request.name,
        password_hash=hash_password.decode(),
        language=Language(request.language),
        province_state=RegionalContext(request.province_state, request.country),
    )
    services.postgres_user_repo.save(user=user)

    profile = ProducerProfile(
        producer_id=user.id,
        producer_types=producer_types,
        name=user.name,
    )
    services.postgres_producer_repo.save(profile)

    token = jwt.encode(
        {
            "user_id": str(user.id),
            "name": user.name,
            "language": user.language.value,
            "province_state": user.province_state.province_state,
            "country": user.province_state.country,
            "exp": datetime.utcnow() + timedelta(hours=24),
        },
        jwt_secret,
        algorithm="HS256",
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login")
def login(request: LoginRequest):
    jwt_secret = os.environ["JWT_SECRET"]
    services = build_services()

    user = (
        services.postgres_user_repo.find_by_email(request.email)
        if request.email
        else services.postgres_user_repo.find_by_phone_number(request.phone_number)
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(request.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {
            "user_id": str(user.id),
            "name": user.name,
            "language": user.language.value,
            "province_state": user.province_state.province_state,
            "country": user.province_state.country,
            "exp": datetime.utcnow() + timedelta(hours=24),
        },
        jwt_secret,
        algorithm="HS256",
    )
    return {"access_token": token, "token_type": "bearer"}
