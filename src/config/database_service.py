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
    pool_size=10,  # Taille du pool de connexions
    max_overflow=20,  # Nombre maximal de connexions supplémentaires qui peuvent être ouvertes au-delà de pool_size
)

AsyncSessionFactory = sessionmaker(
    engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)

async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        logger.info(f"ASYNC Pool: {engine.pool.status()}")
        yield session
