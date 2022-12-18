import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import PostgresDsn

SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# sql = PostgresDsn.build(
#     scheme="postgresql",
#     user="postgres",
#     password="12345678",
#     host="127.0.0.1"
# )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)

Base = declarative_base()

#DB Itilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()