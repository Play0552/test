from fastapi import APIRouter


from app import schemas
from app.config.db.session import PGSession
from app.routers.deps.deps import image_service

router = APIRouter()


@router.post("", response_model=schemas.Msg)
async def register_image(
    image: schemas.CreateImage,
    db: PGSession,
    image_service: image_service,
):
    """
    Регистрация картинки
    """
    await image_service.register(image, db=db)
    return schemas.Msg(msg="Ok")
