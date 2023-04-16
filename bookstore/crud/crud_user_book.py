from bookstore.crud.base import CRUDBase
from bookstore.models import User_Book
from bookstore.schemas import User_BookCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder

class CRUDUser_Book(CRUDBase[User_Book, User_BookCreate, None]):
    async def save_book(self, db:AsyncSession, current_user_id:int, book_id:int) -> User_Book:
        db_obj = User_Book(user_id = current_user_id, book_id = book_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove_saved_book(self, db:AsyncSession, current_user_id:int, book_id:int):
        query = (
            select(User_Book).
            where(User_Book.book_id == book_id and User_Book.user_id == current_user_id)
        )
        result = await db.execute(query)
        await db.delete(result.scalar_one_or_none())
        await db.commit()
        return result

user_book = CRUDUser_Book(User_Book)