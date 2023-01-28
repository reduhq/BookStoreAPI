from typing import Optional
from pydantic import BaseModel
from pydantic import Field, EmailStr

from ..enums.UserEnum import Role, Gender

#Shared properties
class UserBase(BaseModel):
    name:Optional[str] = Field(default=None)
    last_name:Optional[str] = Field(default=None)
    username:Optional[str] = Field(default=None)
    email:Optional[EmailStr] = Field(default=None)

#Properties to receive via API on creation
class UserCreate(UserBase):
    name:str = Field(...)
    last_name:str = Field(...)
    username:str = Field(...)
    email:str = Field(...)
    role:Role = Field(default=None)
    gender:Gender = Field(default=None)
    password:str = Field(...)

#Properties to receive via API on update
class UserUpdate(UserBase):
    password:Optional[str] = Field(default=None)
    gender:Optional[Gender] = Field(default=None)
    role:Optional[Role] = Field(default=None)

class UserInDBBase(UserBase):
    id:int = Field(...)
    role:Role = Field(...)
    gender:Gender = Field(...)
    
    class Config:
        orm_mode = True

#Additional properties to return via API
class User(UserInDBBase):
    ...

#Additional properties stored in DB
class UserInDB(UserInDBBase):
    ...