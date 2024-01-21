import pytest
from httpx import AsyncClient
from pytest_schema import exact_schema
from ..conftest import (
    create_user,
    create_default_url,
    create_custom_url,
    authorization_header,
)
from .schemas import user
from ..urls.schemas import urls_base


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


@pytest.mark.asyncio
async def test_read_current_user_blank_urls_authorized(
    client: AsyncClient, create_user, authorization_header
):
    """
    Testing users without url path authorized
    """
    response = await client.get("/users/me/urls", headers=authorization_header)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_read_current_user_blank_urls_unauthorized(
    client: AsyncClient, create_user
):
    """
    Testing users without url path unauthorized
    """
    response = await client.get("/users/me/urls")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_read_current_user_urls_unauthorized(client: AsyncClient, create_user):
    """
    Testing users with url path unauthorized
    """
    response = await client.get("/users/me/urls")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_read_current_user_urls_authorized(
    client: AsyncClient, create_user, create_default_url, authorization_header
):
    """
    Testing users with url path authorized
    """
    response = await client.get("/users/me/urls", headers=authorization_header)
    assert response.status_code == 200
    assert response.json() != []
    assert exact_schema(urls_base) == response.json()
