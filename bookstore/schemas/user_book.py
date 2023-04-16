from pydantic import BaseModel, Field

class User_BookBase(BaseModel):
    id_user:int = Field(...)
    id_book:int = Field(...)

class User_BookCreate(User_BookBase):
    ...