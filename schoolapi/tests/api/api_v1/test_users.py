import pytest

from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession

from schoolapi.schemas.user import UserCreate
from schoolapi.tests.utils.user import random_email, random_lower_string
from schoolapi import crud
from schoolapi.core.config import settings
from schoolapi.enums.UserEnum import Role

@pytest.mark.asyncio
async def test_get_users_superuser_me(
    client:AsyncClient, superuser_token_headers:dict[str, str]
) -> None:
    r = await client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["role"] == Role.admin.value
    assert current_user["role"] is not Role.teacher.value
    assert current_user["role"] is not Role.student.value
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL

@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client:AsyncClient, normal_user_token_headers:dict[str,str]
) -> None:
    r = await client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user["role"] != Role.admin.value
    assert current_user["role"] != Role.teacher.value
    assert current_user["role"] == Role.student.value
    assert current_user["email"] == settings.EMAIL_TEST_USER

@pytest.mark.asyncio
async def test_create_user_new_email(
    client:AsyncClient, superuser_token_headers:dict[str, str], tmp_db:AsyncSession
) -> None:
    password:str = random_lower_string()
    email:str = random_email()
    data = {
            "name": "user",
            "last_name": "user",
            "username": "user",
            "email": email,
            "role": "student",
            "gender": "masculine",
            "password": password
    }
    r = await client.post(f"{settings.API_V1_STR}/users/", json=data)
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = await crud.user.get_user_by_email(db=tmp_db, email=email)
    assert user
    assert created_user["email"] == user.email

@pytest.mark.asyncio
async def test_get_existing_user(
    client:AsyncClient, tmp_db:AsyncSession
) -> None:
    password:str = random_lower_string()
    email:str = random_email()
    user_in = UserCreate(
            name="user",
            last_name="user",
            username="user",
            email=email,
            role="student",
            gender="masculine",
            password=password
    )
    user = await crud.user.create(db=tmp_db, model=user_in)
    user_id = user.id
    r = await client.get(
        f"{settings.API_V1_STR}/users/{user_id}"
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = await crud.user.get_user_by_email(tmp_db, email=email)
    assert existing_user
    assert api_user["email"] == existing_user.email

@pytest.mark.asyncio
async def test_create_user_existing_email(
    client:AsyncClient, tmp_db:AsyncSession
) -> None:
    email:str = random_email()
    password:str = random_lower_string()
    user_in = UserCreate(
            name="user",
            last_name="user",
            username="user",
            email=email,
            role="student",
            gender="masculine",
            password=password
    )
    await crud.user.create(db=tmp_db, model=user_in)
    data = {
            "name": "user",
            "last_name": "user",
            "username": "user",
            "email": email,
            "role": "student",
            "gender": "masculine",
            "password": password
    }
    r = await client.post(
        f"{settings.API_V1_STR}/users/", json=data
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "id" not in created_user

@pytest.mark.asyncio
async def test_retrieve_users(
    client:AsyncClient, tmp_db:AsyncSession
) -> None:
    email:str = random_email()
    password:str = random_lower_string()
    user_in = UserCreate(
            name="user",
            last_name="user",
            username="user",
            email=email,
            role="student",
            gender="masculine",
            password=password
    )
    await crud.user.create(db=tmp_db, model=user_in)

    
    email2:str = random_email()
    password2:str = random_lower_string()
    user_in2 = UserCreate(
            name="user",
            last_name="user",
            username="user",
            email=email2,
            role="student",
            gender="masculine",
            password=password2
    )
    await crud.user.create(db=tmp_db, model=user_in2)

    r = await client.get(
        f"{settings.API_V1_STR}/users/"
    )
    all_users = r.json()
    assert len(all_users) > 1
    for item in all_users:
        assert item["email"]