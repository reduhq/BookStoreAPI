# Import all the models, so that Base has them before being
# imported by Alembic
from bookstore.db.base_class import Base
from bookstore.models.user import User
from bookstore.models.book import Book
from bookstore.models.user_book import User_Book