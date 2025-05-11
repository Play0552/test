from typing import Annotated

from fastapi import Depends

from app.services.feature.feature import FeatureService, get_feature_service
from app.services.image.image import ImageService, get_image_service
from app.services.worker.worker import WorkerService, get_worker_service


feature_service = Annotated[FeatureService, Depends(get_feature_service)]
image_service = Annotated[ImageService, Depends(get_image_service)]
worker_service = Annotated[WorkerService, Depends(get_worker_service)]
