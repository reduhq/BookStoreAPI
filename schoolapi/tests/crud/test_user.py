from fastapi.encoders import jsonable_encoder 
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from schoolapi.enums.UserEnum import Role
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

@pytest.mark.asyncio
async def test_autenticate_user(tmp_db:AsyncSession) -> None:
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
    authenticated_user = await crud.user.authenticate(tmp_db, email, password)
    assert authenticated_user
    assert user.email == authenticated_user.email

@pytest.mark.asyncio
async def test_not_authenticate_user(tmp_db:AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user = await crud.user.authenticate(tmp_db, email, password)
    assert user == None

@pytest.mark.asyncio
async def test_check_if_user_is_superuser(tmp_db:AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(
        name="user",
        last_name="user",
        username="user",
        email=email,
        role=Role.admin,
        gender="masculine",
        password=password
    )
    user = await crud.user.create(db=tmp_db, model=user_create)
    is_superuser = await crud.user.is_superuser(tmp_db, user)
    assert is_superuser == True

@pytest.mark.asyncio
async def test_check_if_user_is_teacher(tmp_db:AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(
        name="user",
        last_name="user",
        username="user",
        email=email,
        role=Role.teacher,
        gender="masculine",
        password=password
    )
    user = await crud.user.create(tmp_db, user_create)
    is_teacher = await crud.user.is_teacher(tmp_db, user)
    assert is_teacher == True

@pytest.mark.asyncio
async def test_check_if_user_is_student(tmp_db:AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(
        name="user",
        last_name="user",
        username="user",
        email=email,
        role=Role.student,
        gender="masculine",
        password=password
    )
    user = await crud.user.create(tmp_db, user_create)
    is_student = await crud.user.is_student(tmp_db, user)
    assert is_student == True

@pytest.mark.asyncio
async def test_get_user(tmp_db:AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    user_create = UserCreate(
        name="user",
        last_name="user",
        username="user",
        email=email,
        role=Role.student,
        gender="masculine",
        password=password
    )
    user = await crud.user.create(tmp_db, user_create)
    get_user = await crud.user.get(tmp_db, user.id)
    assert get_user
    assert get_user.email == user.email
    assert jsonable_encoder(user) == jsonable_encoder(get_user)