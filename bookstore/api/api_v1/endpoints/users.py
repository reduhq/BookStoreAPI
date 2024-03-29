#FastAPI
from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi import Depends
from fastapi import Body, Path, Query
from fastapi.encoders import jsonable_encoder

#SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

from bookstore.core.config import settings
from bookstore.utils import send_new_account_email
from ....api.deps import get_async_db, get_current_user
from .... import crud, models, schemas

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


router = APIRouter()

@router.post(
    path="/", 
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def create_user(
    db:AsyncSession = Depends(get_async_db),
    user:schemas.UserCreate = Body(...)
):
    db_user = await crud.user.get_user_by_email(db=db, email=user.email) 
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address already exists"
        )
    db_user = await crud.user.create(db=db, model=user)
    if settings.EMAILS_ENABLED and user.email:
        await send_new_account_email(
            email_to=user.email, username=user.username, password=user.password
        )
    return db_user

@router.put(
    path="/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def update_user_me(
    user_in:schemas.UserUpdate = Body(...),
    current_user:models.User = Depends(get_current_user),
    db:AsyncSession = Depends(get_async_db)
) -> models.User:
    """
    Update own user
    """
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get(path="/", response_model=list[schemas.User])
async def get_users(
    db:AsyncSession = Depends(get_async_db),
    skip:int = Query(default=0),
    limit:int = Query(default=5)
):
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get(
    path="/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
) 
async def read_user_me(
    current_user:models.User = Depends(get_current_user)
)-> any:
    """
    Get Current User
    """
    return current_user

@router.get(
    path="/{id}", 
    response_model=schemas.User,
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