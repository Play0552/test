import uuid

from sqlalchemy import Boolean, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.base import Base


IMAGE_SCHEMA = "image"


class Image(Base):
    __tablename__ = "image"
    __table_args__ = {
        "schema": IMAGE_SCHEMA,
    }
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    image: Mapped[str] = mapped_column(
        String, nullable=False, comment="Ссылка на картинку"
    )
    active: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="Флаг доступности картинки"
    )
    features = relationship(
        "Feature",
        secondary="feature.image_x_feature",
        backref="images",
    )
