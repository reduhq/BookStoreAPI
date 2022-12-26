#python

#Pydantic

#FastAPI
from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi import Depends
from fastapi import Body, Path, Query

#SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from ....db.db_setup import get_db, get_async_db
from .... import crud, models, schemas
from ....schemas.user import User, UserCreate

#Models
router = APIRouter()

@router.post(
    path="", 
    response_model=User,
    status_code=status.HTTP_200_OK
)
async def create_user(
    db:AsyncSession = Depends(get_async_db),
    user:UserCreate = Body(...)
):
    db_user = await crud.user.get_user_by_email(db=db, email=user.email) 
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address already exists"
        )
    db_user = await crud.user.create(db=db, model=user)
    return db_user

@router.get(path="", response_model=list[User])
async def get_users(
    db:AsyncSession = Depends(get_async_db),
    skip:int = Query(default=0),
    limit:int = Query(default=5)
):
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get(
    path="/{id}", 
    response_model=User,
    status_code= status.HTTP_200_OK
)
async def get_user_by_id(
    db:AsyncSession = Depends(get_async_db),
    id:int = Path(
        ...,
        gt=0
    )
):
    db_user = await crud.user.get(db=db, id=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist"
        )
    return db_user