from fastapi import Request, HTTPException
from functools import lru_cache
import os
import jwt

url = os.environ["CLERK_JWKS_URL"]

def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(status_code=401)
    token = authorization.split(" ")
    if len(token) != 2 or token[0] != "Bearer":
        raise HTTPException(status_code=401)
    raw_token = token[1]
    try:
        client = get_client()
        signing_key = client.get_signing_key_from_jwt(raw_token)
        return jwt.decode(raw_token, signing_key.key, algorithms=["RS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401)


@lru_cache
def get_client():
        return jwt.PyJWKClient(url)
