from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.repository.base import BaseCRUDRepository
from app.models import Worker
from app.schemas import CreateWorkerDB, UpdateWorker


class WorkerRepository(BaseCRUDRepository[Worker, CreateWorkerDB, UpdateWorker]):
    async def get_by_name(
        self,
        db: AsyncSession,
        name: str,
        custom_options: list[ExecutableOption] = None,
    ) -> Worker:
        query = select(self.model).filter(self.model.name == name)

        if custom_options:
            for custom_option in custom_options:
                if isinstance(custom_option, ExecutableOption):
                    query = query.options(custom_option)

        res = await db.execute(query)
        obj = res.scalars().first()
        return obj


def get_worker_repository():
    return WorkerRepository(Worker)
