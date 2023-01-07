from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from ....api.deps import get_async_db
from .... import schemas, crud, models
from ....core.config import settings
from ....core import security
from ...deps import get_current_user


router = APIRouter()

@router.post(
    path="/login/access-token",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
async def login_access_token(
    db:AsyncSession = Depends(get_async_db),
    form_data:OAuth2PasswordRequestForm = Depends()
):
    user = await crud.user.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, access_token_expires),
        "token_type": "bearer"
    }

@router.post(
    path="/login/test-token",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
async def test_token(current_user:models.User = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user