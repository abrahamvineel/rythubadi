import uvicorn
import os

DEBUG = os.getenv("DEBUG", "false")
reload = DEBUG == "true"

if __name__ == "__main__":
    uvicorn.run("presentation.app:app", host="0.0.0.0", port=8000, reload=reload)
