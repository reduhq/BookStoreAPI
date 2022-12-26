from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from ..db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model:Type[ModelType]):
        self.model = model

    async def get(self, db:AsyncSession, id:any) -> Optional[ModelType]:
        query = (select(self.model).
                where(self.model.id == id))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(self, db:AsyncSession, skip:int = 0, limit:int = 5) -> list[ModelType]:
        query = (select(self.model).
                offset(skip * limit).
                limit(limit))
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db:AsyncSession, model:CreateSchemaType) -> ModelType:
        data_model = jsonable_encoder(model)
        db_model = self.model(**data_model)
        db.add(db_model)
        await db.commit()
        await db.refresh(db_model)
        return db_model