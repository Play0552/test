from pydantic import Field

from app.schemas.base import CoreModel


class BaseWorker(CoreModel):
    name: str = Field(..., description="Название обработчика")
    capacity: int = Field(
        ..., description="Максимальное число картинок для одновременной обработки"
    )


class CreateWorker(BaseWorker):
    features: list[str] = Field(
        ..., min_length=1, description="Список доступных вещей для поиска на картинке"
    )


class CreateWorkerDB(BaseWorker):
    pass


class UpdateWorker(BaseWorker):
    pass
