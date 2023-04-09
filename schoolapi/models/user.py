from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship

from schoolapi.models.user_book import User_Book

from ..db.base_class import Base
from ..enums.UserEnum import Role, Gender


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(Enum(Role), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    password = Column(String(60), nullable=False)

    books = relationship("Book", secondary=User_Book, back_populates="users")