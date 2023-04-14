from typing import Optional
from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi import Body, Query
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from bookstore import models, schemas, crud
from bookstore.api.deps import get_async_db, get_current_user

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
    if not crud.user.is_writer(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user is not allowed to create a book"
        )
    bookdb = await crud.book.create(db, book_in, current_user.id)
    return bookdb

@router.get(
    path='/',
    response_model=list[schemas.Book],
    status_code=status.HTTP_200_OK
)
async def get_books(
    written:bool = Query(default=False),
    saved:Optional[bool] = Query(False),
    limit:int = Query(default=5, ge=0),
    skip:int = Query(default=0, ge=0),
    current_user:models.User = Depends(get_current_user),
    db:AsyncSession = Depends(get_async_db)
) -> list[schemas.Book]:
    if crud.user.is_reader(db, current_user) and written == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is not allowed to use the 'Written' query parameter"
        )
    if crud.user.is_writer(db, current_user) and written == True:
        books = await crud.book.get_written_books(db, current_user.id, limit, skip)
    elif saved:
        books = await crud.book.get_saved_books(db, current_user.id, limit=limit, skip=skip)
    else:
        books = await crud.book.get_multi(db, skip=skip, limit=limit)
    
    return books