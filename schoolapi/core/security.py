from datetime import timedelta, datetime
from typing import Union

from jose import jwt

from ..core.config import settings


ALGORITHM = "HS256"

def create_access_token(
    subject:Union[str,any], expires_delta:timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt