import secrets
from typing import Optional

from pydantic import BaseSettings, validator, EmailStr

class Settings(BaseSettings):
    # JWT
    SECRET_KEY = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRES_MINUTES:int = 1
    
    # Postgres
    DATABASE_HOST:str
    DATABASE_PORT:str
    POSTGRES_PASSWORD:str
    POSTGRES_USER:str
    POSTGRES_DB:str

    # Api
    SQLALCHEMY_DATABASE_URL:Optional[str] = None
    SQLALCHEMY_DATABASE_URL_ASYNC:Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v:Optional[str], values:dict[str, any]) -> str:
        if isinstance(v, str):
            return v
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("DATABASE_HOST")
        port = values.get("DATABASE_PORT")
        db = values.get("POSTGRES_DB")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    @validator("SQLALCHEMY_DATABASE_URL_ASYNC", pre=True)
    def assemble_async_db_connection(cls, v:Optional[str], values:dict[str, any]) -> str:
        if isinstance(v, str):
            return v
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("DATABASE_HOST")
        port = values.get("DATABASE_PORT")
        db = values.get("POSTGRES_DB")
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    # First SuperUser
    FIRST_SUPERUSER_EMAIL:EmailStr
    FIRST_SUPERUSER_PASSWORD:str

    class Config:
        case_sensitive = True


settings = Settings()