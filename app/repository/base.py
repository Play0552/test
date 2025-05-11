from typing import Generic, Type, TypeVar, Sequence

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import Result, select, ClauseElement
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db.base import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUDRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        Базовый CRUD для Postgres
        """
        self.model = model

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        offset: int = 0,
        limit: int = 20,
        custom_options: list[ExecutableOption] | None = None,
        whereclause: ClauseElement | None = None,
    ) -> Sequence[ModelType]:
        """ """

        query = select(self.model)

        if whereclause:
            query = query.where(*whereclause)

        if custom_options:
            for custom_option in custom_options:
                query = query.options(custom_option)

        query = query.offset(offset).limit(limit)

        result: Result = await db.execute(query)
        return result.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType | list[CreateSchemaType],
        relation_objs: dict | None = None,
        with_commit: bool = True,
    ) -> ModelType | list[ModelType]:
        """
        Базовый метод для создания объектов в БД
        """
        try:
            if not isinstance(obj_in, list):
                objs = [obj_in]
            else:
                objs = obj_in
            db_objs = []
            for obj in objs:
                data = obj.model_dump()
                if relation_objs:
                    data.update(relation_objs)
                db_obj = self.model(**data)
                db_objs.append(db_obj)

            db.add_all(db_objs)

            if with_commit:
                await db.commit()
            else:
                await db.flush()

            return db_objs if isinstance(obj_in, list) else db_objs[0]
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="Не уникальные поля при создании"
            )

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        with_commit: bool = True,
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.model_dump(exclude_defaults=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)

            if with_commit:
                await db.commit()
                await db.refresh(db_obj)
            else:
                await db.flush()

            return db_obj
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="Не уникальные поля при обновлении"
            )
