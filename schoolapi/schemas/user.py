from pydantic import BaseModel
from pydantic import Field, EmailStr


#Pydantic Schemas
class UserBase(BaseModel):
    name:str = Field(...)
    email:EmailStr = Field(...)

class UserCreate(UserBase):
    ...

class User(UserBase):
    id:int = Field(...)

    class Config:
        orm_mode = True