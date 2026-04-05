from fastapi import Header, HTTPException

def verify_clerk_jwt(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return authorization[len("Bearer "):]