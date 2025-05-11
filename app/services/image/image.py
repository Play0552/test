from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.image.image import ImageRepository, get_image_repository
from app.repository.feature.feature import FeatureRepository, get_feature_repository
from app.schemas import CreateFeature, CreateImage, CreateImageDB


class ImageService:
    def __init__(
        self,
        image_repository: ImageRepository,
        feature_repository: FeatureRepository,
    ):
        self.image_repository = image_repository
        self.feature_repository = feature_repository

    async def register(self, image: CreateImage, db: AsyncSession) -> None:

        creating_features = [CreateFeature(name=name) for name in image.features]
        await self.feature_repository.create_feature(
            db=db, obj_in=creating_features, with_commit=False
        )

        features = await self.feature_repository.get_by_names(
            db=db, names=image.features
        )

        await self.image_repository.create(
            db=db,
            obj_in=CreateImageDB(
                **image.model_dump(),
            ),
            relation_objs={"features": features},
        )


def get_image_service(
    image_repository: ImageRepository = Depends(get_image_repository),
    feature_repository: FeatureRepository = Depends(get_feature_repository),
):
    return ImageService(image_repository, feature_repository)
