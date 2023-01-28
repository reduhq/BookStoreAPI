from fastapi import Depends
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from schoolapi.tests.utils.utils import random_email, random_lower_string
from schoolapi import crud
from schoolapi.schemas.user import UserCreate

@pytest.mark.asyncio
async def test_create_user(tmp_db:AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(
        name="user",
        last_name="user",
        username="user",
        email=email,
        role="student",
        gender="masculine",
        password=password
    )
    user = await crud.user.create(tmp_db, user_create)
    assert user.email == email
    assert hasattr(user, "password")