from fastapi import APIRouter

from app.api.concrete_note import router as concrete_note_router
from app.api.materials_delivery import router as materials_delivery_router

router = APIRouter()
from dotenv import load_dotenv
load_dotenv()

router.include_router(concrete_note_router, tags=["concrete-note-router"])
router.include_router(materials_delivery_router, tags=["material-delivery-router"])