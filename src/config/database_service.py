from collections.abc import AsyncGenerator
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import *
from loguru import logger

engine = create_async_engine(
    POSTGRES_URL,
    future=True,
    echo=False,
    json_serializer=jsonable_encoder,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionFactory = sessionmaker(
    engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)

async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        logger.info(f"ASYNC Pool: {engine.pool.status()}")
        yield session
