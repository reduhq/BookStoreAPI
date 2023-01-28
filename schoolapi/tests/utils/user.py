from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from schoolapi.tests.utils.utils import random_lower_string, random_email
from schoolapi import crud
from schoolapi.schemas.user import UserCreate, UserUpdate
from schoolapi.models.user import User
from schoolapi.core.config import settings

async def create_random_user(db:AsyncSession) -> User:
    email=random_email()
    password=random_lower_string()
    user_create = UserCreate(
        name="user",
        last_name="user",
        username="user",
        email=email,
        role="student",
        gender="masculine",
        password=password
    )
    user = await crud.user.create(db=db, model=user_create)
    return user

async def user_authentication_header(client:AsyncClient, email:str, password:str) -> dict[str,str]:
    data = {
        "username": email,
        "password": password
    }
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

async def authentication_token_from_email(client:AsyncClient, email:str, db:AsyncSession) -> dict[str, str]:
    """
    Return a valid token for the user with given emain

    If the user doesn't exist it's created first
    """
    password = random_lower_string()
    user = await crud.user.get_user_by_email(email=email, db=db)
    if not user:
        user_create = UserCreate(
            name="user",
            last_name="user",
            username="user",
            email=email,
            role="student",
            gender="masculine",
            password=password
        )
        await crud.user.create(user_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = await crud.user.update(db, user, user_in_update)
    return await user_authentication_header(client=client, email=email, password=password)