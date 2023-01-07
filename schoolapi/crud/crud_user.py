from fastapi.encoders import jsonable_encoder

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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

    # async def is_active(self, db:AsyncSession, user:User):
    #     return user.is_active

user = CRUDUser(User)