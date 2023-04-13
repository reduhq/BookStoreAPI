from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from bookstore.models import Book
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

book = CRUDBook(Book)