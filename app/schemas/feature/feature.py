import uuid

from pydantic import Field

from app.schemas.base import CoreModel


class BaseFeature(CoreModel):
    name: str = Field(..., description="Название предмета")


class Feature(BaseFeature):
    id: uuid.UUID = Field(..., description="Идентификатор предмета")


class CreateFeature(BaseFeature):
    pass


class UpdateFeature(BaseFeature):
    pass
