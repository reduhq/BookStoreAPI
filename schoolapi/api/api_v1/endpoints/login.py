from datetime import timedelta

from fastapi import Body, Depends, APIRouter, Path
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import EmailStr

from ....api.deps import get_async_db
from .... import schemas, crud, models
from ....core.config import settings
from ....core import security
from ...deps import get_current_user
from schoolapi.utils import generate_password_reset_token, send_reset_password_email, verify_password_reset_token
from schoolapi.core.security import get_password_hash


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

@router.post(
    path="/password-recovery/{email}",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK
)
async def recover_password(
    email:EmailStr = Path(...),
    db:AsyncSession = Depends(get_async_db),
) -> any:
    """
    Password Recovery
    """
    user =await crud.user.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist"
        )
    token = await generate_password_reset_token(email=email)
    await send_reset_password_email(email_to=email, email=user.username, token=token)
    return {"msg": "Password recovery email sent"}

@router.post(
    path="/reset-password/",
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK
)
async def reset_password(
    token:str = Body(...),
    new_password:str = Body(...),
    db:AsyncSession = Depends(get_async_db)
) -> any:
    """
    Reset password
    """
    email = await verify_password_reset_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )
    user = await crud.user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username does not exist"
        )
    password = get_password_hash(new_password)
    user.password = password
    db.add(user)
    await db.commit()
    return {"msg": "Password updated succesfully"}