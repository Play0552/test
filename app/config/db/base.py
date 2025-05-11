import sqlalchemy
from sqlalchemy.orm import DeclarativeBase


meta = sqlalchemy.MetaData()


class Base(DeclarativeBase):
    """Base for all models"""

    metadata = meta
