from fastapi import Request, HTTPException

def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    if authorization is None:
        raise HTTPException(status_code=401)
    token = authorization.split(" ")[1]
    #TODO: verify signature with PyJWT + Clerk public key
    return {"sub": "00000000-0000-0000-0000-000000000000"}
