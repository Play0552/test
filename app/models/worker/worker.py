import uuid

from sqlalchemy import Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.base import Base


WORKER_SCHEMA = "worker"


class Worker(Base):
    __tablename__ = "worker"
    __table_args__ = {
        "schema": WORKER_SCHEMA,
    }
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String, unique=True, index=True, comment="Название обработчика"
    )
    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Максимальное число картинок для одновременной обработки",
    )
    features = relationship(
        "Feature",
        secondary="feature.worker_x_feature",
        backref="workers",
    )
