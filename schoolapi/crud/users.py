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

    # def create_user(self, db:Session, user:UserCreate) -> User:
    #     db_user = User(name=user.name, email=user.email)
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user

    # async def get_user_by_id(db:AsyncSession, user_id:int):
    #     query = (select(User).
    #             where(user_id == User.id))
    #     result = await db.execute(query)
    #     return result.scalar_one_or_none()

    # def get_user_by_id(db:Session, user_id:int):
        # return db.query(User).filter(User.id == user_id).first()

    # def get_users(db:Session, skip:int = 0, limit:int =5):
    #     return db.query(User).offset(skip).limit(limit).all()

user = CRUDUser(User)