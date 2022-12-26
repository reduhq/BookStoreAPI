from pydantic import BaseModel
from pydantic import Field, EmailStr


#Shared properties
class UserBase(BaseModel):
    name:str = Field(...)
    email:EmailStr = Field(...)

#Properties to receive via API on creation
class UserCreate(UserBase):
    ...

#Properties to receive via API on update
class UserUpdate(UserBase):
    ...

class UserInDBBase(UserBase):
    id:int = Field(...)
    
    class Config:
        orm_mode = True

#Additional properties to return via API
class User(UserInDBBase):
    ...

#Additional properties stored in DB
class UserInDB(UserInDBBase):
    ...