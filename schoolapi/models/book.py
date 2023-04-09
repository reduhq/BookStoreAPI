from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship

from schoolapi.db.base_class import Base
from schoolapi.models.user_book import User_Book

class Book(Base):
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), index=True, unique=True, nullable=False)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    editorial = Column(String(50), nullable=False)
    pub_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    book_genre = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
    image_url = Column(String(200), nullable=False)

    users = relationship("User", secondary=User_Book, back_populates="books")