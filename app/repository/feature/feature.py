from sqlalchemy import Result, select, Sequence
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Feature
from app.repository.base import BaseCRUDRepository
from app.schemas import CreateFeature, UpdateFeature


class FeatureRepository(BaseCRUDRepository[Feature, CreateFeature, UpdateFeature]):
    async def create_feature(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateFeature | list[CreateFeature],
        with_commit: bool = True,
    ) -> None:
        """

        :param db:
        :param obj_in:
        :param with_commit:
        :return:
        """
        if not isinstance(obj_in, list):
            objs = [obj_in]
        else:
            objs = obj_in

        db_objs = [obj.model_dump() for obj in objs]

        stmt = (
            insert(self.model)
            .values(db_objs)
            .on_conflict_do_nothing(index_elements=["name"])
        )
        await db.execute(stmt)

        if with_commit:
            await db.commit()
        else:
            await db.flush()
        return None

    async def get_by_names(
        self, db: AsyncSession, names: list[str]
    ) -> Sequence[Feature]:
        query = select(self.model).where(self.model.name.in_(names))
        result: Result = await db.execute(query)
        return result.scalars().all()


def get_feature_repository() -> FeatureRepository:
    return FeatureRepository(Feature)
