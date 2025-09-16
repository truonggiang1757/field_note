import os
import logging
import time
from typing import Tuple
import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.models.concrete_note import ConcreteExtractRequest, ConcreteExtractResponse, ConcreteExtractStatus
from app.services.concrete_note import ConcreteNoteService

logger = logging.getLogger(__name__)

router = APIRouter()

async def download_image(file_url: str) -> Tuple[bytes, str]:
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", file_url, follow_redirects=True, timeout=30.0) as response:
                response.raise_for_status()

                # 1. Validate Content-Type is an image
                content_type = response.headers.get("Content-Type", "")
                if not content_type.startswith("image/"):
                    logger.warning(f"File from {file_url} is not an image. Content-Type: {content_type}")
                    raise HTTPException(
                        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                        detail=f"URL does not point to a valid image file. Content-Type received: {content_type}"
                    )
                
                # 2. Validate Size
                file_content = await response.aread()
                if len(file_content) > settings.MAX_FILE_SIZE_BYTES:
                    logger.warning(f"Image from {file_url} denied due to size. Size: {len(file_content)} bytes, Max: {settings.MAX_FILE_SIZE_BYTES} bytes.")
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Image file size exceeds the maximum limit of {settings.MAX_FILE_SIZE_MB} MB."
                    )

                filename = os.path.basename(httpx.URL(file_url).path.split('?')[0]) or "downloaded_image"
                logger.info(f"Successfully downloaded image '{filename}' from '{file_url}'. Size: {len(file_content)} bytes.")
                return file_content, filename

    except httpx.RequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not retrieve image from URL: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching image from the provider: {e.response.status_code}")
    except httpx.InvalidURL:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file URL provided.")
    except Exception as e:
        logger.error(f"Unexpected error during image download from {file_url}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected server error occurred during file download.")

def get_service(request: ConcreteExtractRequest) -> ConcreteNoteService:
    return ConcreteNoteService(model_name=request.model_name)

@router.post("/concrete_note", response_model=ConcreteExtractResponse)
async def concrete_extract(
    request: ConcreteExtractRequest,
    service: ConcreteNoteService = Depends(get_service)
):
    start_time = time.monotonic()

    try:
        file_content, _ = await download_image(request.file_url)
        result_json = await service.process_file(file_content=file_content)

        elapsed_time = time.monotonic() - start_time
        logger.info(f"Successfully processed concrete note from {request.file_url} in {elapsed_time:.2f}s")
        return ConcreteExtractResponse(
            status=ConcreteExtractStatus.SUCCESS,
            data=result_json,
            processing_time=elapsed_time
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        elapsed_time = time.monotonic() - start_time
        error_message = f"An unexpected error occurred: {str(e)}"
        logger.error(f"Failed to process {request.file_url}: {error_message}", exc_info=True)

        return ConcreteExtractResponse(
            status=ConcreteExtractStatus.ERROR,
            data=None,
            processing_time=elapsed_time,
            error_message=error_message
        )