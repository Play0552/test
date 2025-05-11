from fastapi import APIRouter, Query, BackgroundTasks

from app import schemas
from app.config.db.session import PGSession, RedisClient
from app.routers.deps.deps import worker_service
from app.services.utils import process_image

router = APIRouter()


@router.post("", response_model=schemas.Msg)
async def register_worker(
    worker: schemas.CreateWorker,
    db: PGSession,
    worker_service: worker_service,
):
    """
    Регистрация обработчика
    """
    await worker_service.register(db=db, worker=worker)
    return schemas.Msg(msg="Ok")


@router.get("", response_model=list[schemas.Image])
async def get_list_images(
    db: PGSession,
    redis_client: RedisClient,
    worker_service: worker_service,
    background_tasks: BackgroundTasks,
    name: str = Query(...),
):
    """
    Получение списка доступных для обработки картинок
    """
    worker = await worker_service.get_worker_with_features(db=db, worker_name=name)
    worker_id = worker.id
    images = await worker_service.assign_images_to_worker(
        db=db, worker=worker, redis_client=redis_client
    )
    for image in images:
        background_tasks.add_task(process_image, str(image.id), str(worker_id))
    return images
