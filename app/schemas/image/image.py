import uuid
from typing import Optional

from pydantic import Field

from app.schemas.base import CoreModel


class ImageBase(CoreModel):
    image: str = Field(..., description="Ссылка на картинку")


class CreateImage(ImageBase):
    features: list[str] = Field(..., min_length=1, description="Список для поиска")


class CreateImageDB(ImageBase):
    pass


class UpdateImage(CoreModel):
    active: Optional[bool] = Field(
        default=None, description="Флаг доступности картинки"
    )


class Image(ImageBase):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Идентификатор картинки"
    )
