from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi import Body
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from bookstore import models, schemas
from bookstore.api.deps import get_async_db, get_current_user
from bookstore.crud.crud_book import book
from bookstore.crud.crud_user import user

router = APIRouter()

@router.post(
    path="/",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK
)
async def create_book(
    current_user:models.User = Depends(get_current_user),
    book_in:schemas.BookCreate = Body(...),
    db:AsyncSession = Depends(get_async_db)
):
    """
    Creating a new book
    """
    if not user.is_writer(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user is not allowed to create a book"
        )
    bookdb = await book.create(db, book_in, current_user.id)
    return bookdb