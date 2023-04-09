from sqlalchemy import Column, Integer, ForeignKey
from schoolapi.db.base_class import Base

class User_Book(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    book_id = Column(Integer, ForeignKey("book.id"))