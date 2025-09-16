import logging
import time
from fastapi import APIRouter, Depends, HTTPException

from app.models.materials_delivery import MaterialsDeliveryRequest, MaterialsDeliveryResponse, ExtractStatus
from app.services.materials_delivery import MaterialsDeliveryService
from app.api.concrete_note import download_image


logger = logging.getLogger(__name__)

router = APIRouter()

def get_service() -> MaterialsDeliveryService:
    """Dependency injector for the materials delivery service."""
    return MaterialsDeliveryService()

@router.post("/materials_delivery", response_model=MaterialsDeliveryResponse)
async def materials_delivery(
    request: MaterialsDeliveryRequest,
    service: MaterialsDeliveryService = Depends(get_service)
):
    start_time = time.monotonic()

    try:
        file_content, _ = await download_image(request.file_url)
        result_json = await service.process_file(file_content=file_content)

        elapsed_time = time.monotonic() - start_time
        logger.info(f"Successfully processed materials delivery note from {request.file_url} in {elapsed_time:.2f}s")
        
        return MaterialsDeliveryResponse(
            status=ExtractStatus.SUCCESS,
            data=result_json,
            processing_time=elapsed_time
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        elapsed_time = time.monotonic() - start_time
        error_message = f"An unexpected error occurred: {str(e)}"
        logger.error(f"Failed to process {request.file_url}: {error_message}", exc_info=True)

        return MaterialsDeliveryResponse(
            status=ExtractStatus.ERROR,
            data=None,
            processing_time=elapsed_time,
            error_message=error_message
        )