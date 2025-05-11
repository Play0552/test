import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db.base import Base

FEATURE_SCHEMA = "feature"


class Feature(Base):
    __tablename__ = "feature"
    __table_args__ = {
        "schema": FEATURE_SCHEMA,
    }
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, unique=True, comment="Название предмета")


class WorkerXFeature(Base):
    __tablename__ = "worker_x_feature"
    __table_args__ = {
        "schema": FEATURE_SCHEMA,
    }
    worker_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("worker.worker.id"), primary_key=True, index=True
    )
    feature_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("feature.feature.id"), primary_key=True
    )


class ImageXFeature(Base):
    __tablename__ = "image_x_feature"
    __table_args__ = {
        "schema": FEATURE_SCHEMA,
    }
    image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("image.image.id"), primary_key=True, index=True
    )
    feature_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("feature.feature.id"), primary_key=True, index=True
    )
