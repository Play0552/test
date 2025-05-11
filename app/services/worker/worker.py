from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Worker
from app.repository.image.image import ImageRepository, get_image_repository
from app.repository.worker.worker import WorkerRepository, get_worker_repository
from app.repository.feature.feature import FeatureRepository, get_feature_repository
from app.schemas import CreateWorker, CreateFeature, CreateWorkerDB, UpdateImage


class WorkerService:
    def __init__(
        self,
        worker_repository: WorkerRepository,
        feature_repository: FeatureRepository,
        image_repository: ImageRepository,
    ):
        self.worker_repository = worker_repository
        self.feature_repository = feature_repository
        self.image_repository = image_repository

    async def register(self, db: AsyncSession, worker: CreateWorker) -> None:

        creating_features = [CreateFeature(name=name) for name in worker.features]
        await self.feature_repository.create_feature(
            db=db, obj_in=creating_features, with_commit=False
        )

        features = await self.feature_repository.get_by_names(
            db=db, names=worker.features
        )

        await self.worker_repository.create(
            db=db,
            obj_in=CreateWorkerDB(**worker.model_dump()),
            relation_objs={"features": features},
        )

    @staticmethod
    async def check_capacity(redis_client: Redis, worker: Worker) -> int or None:
        """
        Проверка доступности обработчика
        """
        current = int(await redis_client.get(f"worker:{worker.id}:load") or 0)
        available = worker.capacity - current
        if available <= 0:
            return None
        return available

    @staticmethod
    async def load_worker(redis_client: Redis, worker: Worker):
        await redis_client.incr(f"worker:{worker.id}:load")

    async def get_worker_with_features(
        self, db: AsyncSession, worker_name: str
    ) -> Worker:
        custom_options = [selectinload(Worker.features)]
        worker = await self.worker_repository.get_by_name(
            db=db, name=worker_name, custom_options=custom_options
        )
        return worker

    async def assign_images_to_worker(
        self,
        db: AsyncSession,
        worker: Worker,
        redis_client: Redis,
    ):
        """
        Поиск доступных картинок
        """
        limit = await self.check_capacity(redis_client=redis_client, worker=worker)
        if not limit:
            return []
        images = await self.image_repository.get_avaliable_images(
            db=db, worker=worker, limit=limit
        )
        total = len(images)
        updated_images = []
        for num, img in enumerate(images):
            last = num == total - 1
            updated_image = await self.image_repository.update(
                db=db,
                db_obj=img,
                obj_in=UpdateImage(active=False),
                with_commit=last,
            )
            updated_images.append(updated_image)
            await self.load_worker(redis_client=redis_client, worker=worker)

        return updated_images


def get_worker_service(
    worker_repository: WorkerRepository = Depends(get_worker_repository),
    feature_repository: FeatureRepository = Depends(get_feature_repository),
    image_repository: ImageRepository = Depends(get_image_repository),
):
    return WorkerService(worker_repository, feature_repository, image_repository)
