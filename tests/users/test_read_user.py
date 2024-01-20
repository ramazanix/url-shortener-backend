import pytest
from httpx import AsyncClient
from pytest_schema import exact_schema
from ..conftest import create_user, authorization_header
from .schemas import user


@pytest.mark.asyncio
async def test_read_current_user_authorized(
    client: AsyncClient, create_user, authorization_header
):
    """
    Testing users path access authorized
    """
    response = await client.get("/users/me", headers=authorization_header)
    assert response.status_code == 200
    assert exact_schema(user) == response.json()
    assert response.json().get("username") == "username"


@pytest.mark.asyncio
async def test_read_current_user_unauthorized(client: AsyncClient):
    """
    Testing users path access unauthorized
    """
    response = await client.get("/users/me")
    assert response.status_code == 401
