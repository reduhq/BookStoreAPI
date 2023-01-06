from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

from .base import CRUDBase

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_user_by_email(self, db:AsyncSession, email:str) -> Optional[User]:
        query = (select(User).
                        where(User.email == email))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def authenticate(self, db:AsyncSession, email:str, password:str) -> Optional[User]:
        user = await self.get_user_by_email(db, email)
        if not user:
            return None
        if not user.password == password:
            return None
        return User

    # async def is_active(self, db:AsyncSession, user:User):
    #     return user.is_active

user = CRUDUser(User)