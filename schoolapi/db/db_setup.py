import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from ..core.config import settings

# ----- ASYNC ENGINE -----
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL_ASYNC, future=True
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
#DB Itilities
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()

