from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from presentation.routes.health import router as health_router
from presentation.routes.market_listing import router as listing_router
from presentation.routes.chat import router as chat_router
from presentation.routes.diagnose import router as diagnose_router
from presentation.routes.scheme import router as scheme_router
from presentation.routes.voice import router as voice_router
from presentation.routes.upload import router as upload_router
from presentation.routes.auth import router as auth_router
from presentation.routes.conversations import router as conversations_router
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from pathlib import Path
DEBUG = os.getenv("DEBUG", "false")

docs = "/docs" if DEBUG == "true" else None
redoc = "/redoc" if DEBUG == "true" else None

app = FastAPI(docs_url=docs, redoc_url=redoc)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    return response

app.include_router(health_router)
app.include_router(listing_router)
app.include_router(chat_router)
app.include_router(diagnose_router)
app.include_router(scheme_router)
app.include_router(voice_router)
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(conversations_router)
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
