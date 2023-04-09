from fastapi.encoders import jsonable_encoder

from typing import Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bookstore.enums.UserEnum import Role
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password

from .base import CRUDBase

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db:AsyncSession, model:UserCreate) -> User:
        data_model =  jsonable_encoder(model)
        user = User(**data_model)
        user.password = get_password_hash(model.password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update(self, db:AsyncSession, *, db_obj:User, obj_in:Union[UserUpdate, dict[str, any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            if update_data["password"]:
                hashed_password = get_password_hash(update_data["password"])
                update_data["password"] = hashed_password
        return await super().update(db,db_obj=db_obj, obj_in=update_data)

    async def get_user_by_email(self, db:AsyncSession, email:str) -> Optional[User]:
        query = (select(User).
                        where(User.email == email))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def authenticate(self, db:AsyncSession, email:str, password:str) -> Optional[User]:
        user = await self.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    async def is_superuser(self, db:AsyncSession, model:User) -> bool:
        return model.role == Role.admin

    async def is_reader(self, db:AsyncSession, model:User) -> bool:
        return model.role == Role.reader

    async def is_writer(self, db:AsyncSession, model:User) -> bool:
        return model.role == Role.writer

    # async def is_active(self, db:AsyncSession, user:User):
    #     return user.is_active

user = CRUDUser(User)