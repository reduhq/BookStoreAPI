from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from datetime import date

class BookBase(BaseModel):
    title:Optional[str] = Field(None)
    author:Optional[str] = Field(None)
    editorial:Optional[str] = Field(None)
    description:Optional[str] = Field(None)
    book_genre:Optional[str] = Field(None)
    language:Optional[str] = Field(None)
    image_url:Optional[str] = Field(None)

class BookCreate(BookBase):
    isbn:str = Field(...)
    title:str = Field(...)
    author:str = Field(...)
    editorial:str = Field(...)
    description:str = Field(...)
    book_genre:str = Field(...)
    language:str = Field(...)
    image_url:str = Field(...)

class BookUpdate(BookBase):
    ...

class BookInDBBase(BookBase):
    id:int = Field(...)
    isbn:str = Field(...)
    pub_date:date = Field(...)
    writer_id:int = Field(...)

    class Config:
        orm_mode = True

class Book(BookInDBBase):
    ...

class BookInDB(BookInDBBase):
    ...

