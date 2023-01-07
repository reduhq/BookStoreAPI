from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from pydantic import ValidationError

from ..db.db_setup import AsyncSessionLocal
from ..import crud, models, schemas
from ..core.config import settings
from ..core import security

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl = "/login/access-token"
)

#DB Utilities
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()


async def get_current_user(
    db:AsyncSession = Depends(get_async_db), token:str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=security.ALGORITHM
        )
        token_data = schemas.TokenPayload(**payload)
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found"
        )
    return user