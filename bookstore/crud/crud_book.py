from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import join
from sqlalchemy.orm import joinedload

from datetime import datetime

from bookstore.models import Book, User_Book
from bookstore.schemas import BookCreate, BookUpdate
from bookstore.crud.base import CRUDBase

class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    async def create(self, db: AsyncSession, obj_in:BookCreate, writer_id:int) -> Book:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, writer_id = writer_id, pub_date=datetime.now().date()) 
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_saved_books(self, db: AsyncSession, current_user_id:int, limit:int = 5, skip:int = 0) -> list[Book]:
        query = (
            select(Book).#options(joinedload(Book.writer)).
            offset(skip * limit).
            limit(limit).
            select_from(join(User_Book, Book, User_Book.book_id == Book.id)).
            where(User_Book.user_id == current_user_id)            
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_written_books(self, db:AsyncSession, current_user_id:int, limit:int = 5, skip:int = 0) -> list[Book]:
        query = (
            select(Book).
            where(Book.writer_id == current_user_id)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def remove_written_book(self, db:AsyncSession, book_id:int):
        return await super().remove(db, id=book_id) 

book = CRUDBook(Book)