import pytest
from httpx import AsyncClient
from pytest_schema import exact_schema
from ..conftest import (
    create_user,
    create_default_url,
    authorization_header,
)
from ..urls.schemas import url_base


@pytest.mark.asyncio
async def test_read_url_unauthorized(
    client: AsyncClient, create_user, create_default_url
):
    """
    Trying to read url unauthorized
    """
    response = await client.get(f"/urls/{create_default_url['short_name']}")
    assert response.status_code == 200
    assert response.json() == exact_schema(url_base)


@pytest.mark.asyncio
async def test_read_url_authorized(
    client: AsyncClient, create_user, create_default_url
):
    """
    Trying to read url authorized
    """
    response = await client.get(f"/urls/{create_default_url['short_name']}")
    assert response.status_code == 200
    assert response.json() == exact_schema(url_base)
