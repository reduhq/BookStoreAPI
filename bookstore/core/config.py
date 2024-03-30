import secrets
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, validator, EmailStr

class Settings(BaseSettings):
    PROJECT_NAME:str
    API_V1_STR: str = "/api/v1"
    SERVER_HOST:AnyHttpUrl
    
    # JWT
    SECRET_KEY = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRES_MINUTES:int = 30
    
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
    EMAIL_TEST_USER:EmailStr = "test@example.com"
    FIRST_SUPERUSER_EMAIL:EmailStr
    FIRST_SUPERUSER_PASSWORD:str

    # Email - SMTP
    SMTP_TLS:bool = True
    SMTP_HOST:Optional[str] = None
    SMTP_PORT:Optional[int] = None
    SMTP_USER:Optional[str] = None
    SMTP_PASSWORD:Optional[str] = None
    EMAILS_FROM_EMAIL:Optional[EmailStr] = None
    EMAILS_FROM_NAME:Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v:Optional[str], values:dict[str, any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS:int = 48
    EMAIL_TEMPLATES_DIR:str = "/BookStore/bookstore/email-templates/build"
    EMAILS_ENABLED:bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v:bool, values:dict[str, any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )
    
    # Cloudinary
    CLOUD_NAME:str
    API_KEY:str
    API_SECRET:str 

    class Config:
        case_sensitive = True


settings = Settings()