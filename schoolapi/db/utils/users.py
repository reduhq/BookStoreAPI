from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.user import User
from ...schemas.user import UserCreate

async def get_user_by_id(db:AsyncSession, user_id:int):
    query = (select(User).
            where(user_id == User.id))
    result = await db.execute(query)
    return result.scalar_one_or_none()

# def get_user_by_id(db:Session, user_id:int):
    # return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def get_users(db:Session, skip:int = 0, limit:int =5):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db:Session, user:UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user