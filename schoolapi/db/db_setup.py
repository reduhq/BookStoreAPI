import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

SQLALCHEMY_DATABASE_URL_ASYNC = os.environ.get('SQLALCHEMY_DATABASE_URL_ASYNC')

# ----- ASYNC ENGINE -----
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC, future=True
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
#DB Itilities
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()

