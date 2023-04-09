from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from bookstore.core.config import settings

# ----- ASYNC ENGINE -----
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL_ASYNC, pool_pre_ping=True
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, autoflush=False, autocommit=False
)