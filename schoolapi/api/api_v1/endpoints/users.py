#python

#Pydantic

#FastAPI
from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi import Depends
from fastapi import Body, Path, Query

#SQLAlchemy
from sqlalchemy.orm import Session

from ....db.db_setup import get_db
from ....db.utils import users
from ....schemas.user import User, UserCreate

#Models
router = APIRouter()

@router.post(
    path="", 
    response_model=UserCreate,
    status_code=status.HTTP_200_OK
)
async def create_user(
    db:Session = Depends(get_db),
    user:UserCreate = Body(...)
):
    db_user = users.get_user_by_email(db=db, email=user.email) 
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address already exists"
        )
    return db_user

@router.get(path="", response_model=list[User])
async def get_users(
    db:Session = Depends(get_db),
    skip:int = Query(default=0),
    limit:int = Query(default=5)
):
    return users.get_users(db, skip=skip, limit=limit)

@router.get(
    path="/{id}", 
    response_model=User,
    status_code= status.HTTP_200_OK
)
async def get_user_by_id(
    db:Session = Depends(get_db),
    id:int = Path(
        ...,
        gt=0
    )
):
    db_user = users.get_user_by_id(db=db, user_id=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist"
        )
    return db_user

# @router.get(path="/name/{name}")
# def get_user_by_name(name:str = Path(...)):
#     return [user for user in users if user.name == name]