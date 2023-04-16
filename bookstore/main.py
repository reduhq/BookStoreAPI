from fastapi import FastAPI

from bookstore.api.api_v1.api import api_router
from bookstore.core.config import settings

# user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookStore API",
    openapi_url=f"{settings.API_V1_STR}/openai.json",
    description="",
    version="0.0.1",
    contact={
        "Name": "Rey Halsall",
        "Email": "reyeduardohalsallquintero8@gmail.com",
    },
)

app.include_router(api_router, prefix=settings.API_V1_STR)