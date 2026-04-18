from fastapi import APIRouter, HTTPException
from presentation.schemas.register_request import RegisterRequest
from presentation.schemas.login_request import LoginRequest
from domain.user import User
from bootstrap import build_services
import uuid
from datetime import datetime, timedelta
import bcrypt 
import jwt
import os
JWT_SECRET = os.environ["JWT_SECRET"]

router = APIRouter()

@router.post("/auth/register")
def register(request: RegisterRequest):
    repo = build_services().postgres_user_repo
    existing = repo.find_by_email(request.email) if request.email else repo.find_by_phone_number(request.phone_number)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Account already exists")

    hash_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
    user = User(uuid.uuid4(), 
                request.email,
                request.phone_number,
                request.name,
                hash_password.decode())
    repo.save(user=user)

    token = jwt.encode({"user_id": str(user.id), "name": user.name,
                        "exp": datetime.utcnow() + timedelta(hours=24)},
                        JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login")
def login(request: LoginRequest):
    repo = build_services().postgres_user_repo
    user = repo.find_by_email(request.email) if request.email else repo.find_by_phone_number(request.phone_number)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(request.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"user_id": str(user.id), "name": user.name,
                        "exp": datetime.utcnow() + timedelta(hours=24)},
                        JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}    
