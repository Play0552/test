from pydantic import BaseModel, ConfigDict


class CoreModel(BaseModel):
    """
    Базовая pydantic схема
    """

    model_config = ConfigDict(from_attributes=True)
