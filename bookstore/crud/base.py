from typing import Generic, Optional, Type, TypeVar, Union

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

    async def update(self, db:AsyncSession, *, db_obj:ModelType, obj_in:Union[UpdateSchemaType, dict[str, any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in,dict):
            update_data = obj_in
        else: 
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db:AsyncSession, *, id:int) -> ModelType:
        query = (
            select(self.model).
            where(self.model.id == id)
        )
        result = await db.execute(query)
        await db.delete(result.scalar_one_or_none())
        await db.commit()
        return result