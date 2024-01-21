import pytest
from httpx import AsyncClient
from pytest_schema import exact_schema
from ..conftest import (
    create_user,
    create_default_url,
    authorization_header,
)


@pytest.mark.asyncio
async def test_delete_current_user_url_authorized(
    client: AsyncClient, create_user, authorization_header, create_default_url
):
    """
    Trying to delete current user with auth
    """
    response = await client.delete(f"/urls/{create_default_url['short_name']}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_current_user_not_existed_url(
    client: AsyncClient, create_user, authorization_header, create_default_url
):
    """
    Trying to delete current user with auth
    """
    response = await client.delete(f"/urls/not-exists")
    assert response.status_code == 400
