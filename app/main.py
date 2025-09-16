from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api import router as api_router
from app.middleware.api_key import APIKeyMiddleware

from app.core.config import settings
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(APIKeyMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["status"])
async def root():
    """Root endpoint to check API status"""
    return {
        "message": f"{settings.APP_NAME} is running",
        "status": "OK",
        "services": ["CV Scoring", "Job Description", "CV Parsing", "Interview Questions"]
    }

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.DESCRIPTION,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 