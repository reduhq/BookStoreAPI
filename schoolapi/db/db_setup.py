import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from pydantic import PostgresDsn

SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
SQLALCHEMY_DATABASE_URL_ASYNC = os.environ.get('SQLALCHEMY_DATABASE_URL_ASYNC')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
#DB Itilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- ASYNC ENGINE -----
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL_ASYNC
)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
#DB Itilities
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()

Base = declarative_base()
