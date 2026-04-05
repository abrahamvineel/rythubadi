from fastapi import FastAPI
from presentation.routes.health import router as health_router
from presentation.routes.market_listing import router as listing_router
from presentation.routes.chat import router as chat_router
import os
import uuid
DEBUG = os.getenv("DEBUG", "false")

docs = "/docs" if DEBUG == "true" else None
redoc = "/redoc" if DEBUG == "true" else None

app = FastAPI(docs_url=docs, redoc_url=redoc)
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
