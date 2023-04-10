from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from bookstore.db.base_class import Base

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
    writer_id = Column(Integer, ForeignKey("user.id"))

    writer = relationship("User", back_populates="published_books")
    users = relationship("User", secondary="user_book", back_populates="books")