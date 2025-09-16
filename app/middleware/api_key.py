import logging
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

logger = logging.getLogger(__name__)

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bỏ qua route OpenAPI, docs và root
        if request.url.path.startswith("/docs") or \
           request.url.path.startswith("/redoc") or \
           request.url.path.startswith("/api/v1/openapi.json") or \
           request.url.path == "/":
            return await call_next(request)

        api_key = request.headers.get(settings.API_KEY_NAME)
        logger.info("request ",  list(request.headers.keys()))

        if api_key != settings.API_KEY:
            logger.info("Invalid API Key")
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Invalid or missing API Key"
            # )
        return await call_next(request)
