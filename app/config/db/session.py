from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from redis.asyncio import Redis

from app.config.settings import settings

# PostgresSQL
engine = create_async_engine(
    settings.POSTGRES_DATABASE_URI.unicode_string(),
    pool_pre_ping=True,
)
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


PGSession = Annotated[AsyncSession, Depends(get_db)]

# Redis
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


async def get_redis() -> AsyncGenerator[Redis, None]:
    try:
        yield redis_client
    finally:
        await redis_client.close()


RedisClient = Annotated[Redis, Depends(get_redis)]
