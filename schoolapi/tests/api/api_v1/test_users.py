import pytest

from httpx import AsyncClient

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
