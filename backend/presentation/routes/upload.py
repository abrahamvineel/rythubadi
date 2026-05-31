import os, uuid
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from presentation.dependencies.auth import get_current_user_id

router = APIRouter()

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_SIZE = 5 * 1024 * 1024 #5MB

@router.post("/upload")
async def upload_image(file: UploadFile, user_id: str = Depends(get_current_user_id)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported image format")
    
    data = await file.read()

    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Image too large")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(data)

    return {"url": f"http://localhost:8000/uploads/{filename}"}
