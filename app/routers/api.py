from fastapi import APIRouter

from .image.image import router as image_router
from .worker.worker import router as worker_router

api_router = APIRouter()

api_router.include_router(image_router, prefix="/image", tags=["image"])
api_router.include_router(worker_router, prefix="/worker", tags=["worker"])
