from sqlalchemy.ext.asyncio import AsyncSession
from schoolapi import crud, schemas
from schoolapi.core.config import settings
from schoolapi.db import base

# make sure all SQL Alchemy models are imported (schoolapi.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = await crud.user.get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            name="admin",
            last_name="admin",
            email=settings.FIRST_SUPERUSER_EMAIL,
            gender="masculine",
            role="admin",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            username="admin"
        )
        user = await crud.user.create(db, model=user_in)