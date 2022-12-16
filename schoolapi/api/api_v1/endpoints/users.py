#python

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import APIRouter
from fastapi import Body, Path


#Models
router = APIRouter()

class User(BaseModel):
    name:str = Field(...)
    email:EmailStr = Field(...)
    is_active:bool = Field(...)


#CRUD
users:list[User] = []

@router.post(path="/")
def create_user(user:User = Body(...)):
    users.append(user)
    return {"response": f"{user.name}'s account was created succesfully, with id = {len(users)-1}"}

@router.get(path="/")
def get_all_users():
    return list(map(lambda x: x, users))

@router.get(path="/id/{id}")
def get_user_by_id(id:int = Path(...)):
    return users[id]

@router.get(path="/name/{name}")
def get_user_by_name(name:str = Path(...)):
    return [user for user in users if user.name == name]