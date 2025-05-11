from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models import Image, WorkerXFeature, Worker, ImageXFeature
from app.repository.base import BaseCRUDRepository
from app.schemas import CreateImageDB, UpdateImage


class ImageRepository(BaseCRUDRepository[Image, CreateImageDB, UpdateImage]):
    async def get_avaliable_images(
        self, db: AsyncSession, worker: Worker, limit: int
    ) -> Sequence[Image]:
        WF = aliased(WorkerXFeature)
        W = aliased(Worker)
        IMF = aliased(ImageXFeature)
        IMG = aliased(Image)
        features_cte = (
            select(WF.feature_id.label("id"))
            .join(W, WF.worker_id == W.id)
            .where(W.name == worker.name)
            .cte("features")
        )

        query = (
            select(IMG)
            .join(IMF, IMF.image_id == IMG.id)
            .outerjoin(features_cte, features_cte.c.id == IMF.feature_id)
            .where(IMG.active.is_(True))
            .group_by(IMG.id)
            .having(func.count().label("total") - func.count(features_cte.c.id) == 0)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()


def get_image_repository() -> ImageRepository:
    return ImageRepository(Image)
