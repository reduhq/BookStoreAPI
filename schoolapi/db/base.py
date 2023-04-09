# Import all the models, so that Base has them before being
# imported by Alembic
from schoolapi.db.base_class import Base
from schoolapi.models.user import User
from schoolapi.models.book import Book
from schoolapi.models.user_book import User_Book