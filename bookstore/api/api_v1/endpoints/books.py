from typing import Optional
from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi import Body, Query, Path, UploadFile, File
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
    isbn:str,
    title:str,
    author:str,
    editorial:str,
    description:str,
    book_genre:str,
    language:str,
    image:UploadFile = File(...),
    current_user:models.User = Depends(get_current_user),
    db:AsyncSession = Depends(get_async_db)
):
    """
    Creating a new book (Only writers)
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

@router.put(
    path="/{id}",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK
)
async def update_book(
    db:AsyncSession = Depends(get_async_db),
    book_upd:schemas.BookUpdate = Body(...),
    id:int = Path(...),
    current_user:models.User = Depends(get_current_user)
) -> schemas.Book:
    """
    Updating a book (Only writers)
    """
    if not crud.user.is_writer(db, current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user is not allowed to update a book"
        )
    book_bd = await crud.book.get(db, id)
    if not book_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    book_bd = await crud.book.update(db, db_obj=book_bd, obj_in=book_upd)
    return book_bd

@router.post(
    path='/save/{id}',
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK
)
async def save_book(
    db:AsyncSession = Depends(get_async_db),
    id:int = Path(...),
    current_user:models.User = Depends(get_current_user)
) -> schemas.Msg:
    book_db = await crud.book.get(db, id)
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    await crud.user_book.save_book(db, current_user.id, id)
    return {'msg': "The Book has been saved successfully"}

@router.delete(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Msg
)
async def remove_book(
    saved:bool = Query(False),
    written:bool = Query(False),
    db:AsyncSession = Depends(get_async_db),
    current_user:models.User = Depends(get_current_user),
    id:int = Path(...)
) -> schemas.Msg:
    if crud.user.is_reader(db, current_user) and written == True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user is not allowed to use the 'Written' query parameter"
        )
    book = await crud.book.get(db, id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    if saved:
        await crud.user_book.remove_saved_book(db, current_user.id, id)
    elif written:
        await crud.book.remove_written_book(db, id)
    return {"msg": "The book has been removed successfully"}