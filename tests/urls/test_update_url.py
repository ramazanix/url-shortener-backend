import pytest
from httpx import AsyncClient
from pytest_schema import exact_schema
from .schemas import url
from ..conftest import (
    url_default_data,
    url_custom_data,
    create_default_url,
    create_custom_url,
)


@pytest.mark.asyncio
async def test_update_url_short_name(
    client: AsyncClient, create_user, create_default_url
):
    """
    Trying to update short_name url
    """
    response = await client.patch(
        f"/urls/{create_default_url['short_name']}",
        json={"short_name": "new-short-name"},
    )
    assert response.status_code == 200
    assert response.json() == exact_schema(url)


@pytest.mark.asyncio
async def test_update_url_full_name(
    client: AsyncClient, create_user, create_default_url
):
    """
    Trying to update full_name url
    """
    response = await client.patch(
        f"/urls/{create_default_url['short_name']}",
        json={"full_name": "https://example2.com"},
    )
    assert response.status_code == 200
    assert response.json() == exact_schema(url)


@pytest.mark.asyncio
async def test_update_url_blank_data(
    client: AsyncClient, create_user, create_default_url, authorization_header
):
    """
    Trying to update url with blank data
    """
    response = await client.patch(
        f"/urls/{create_default_url['short_name']}",
        json={},
        headers=authorization_header,
    )
    assert response.status_code == 400
    assert response.json() != exact_schema(url)


@pytest.mark.asyncio
async def test_update_url_invalid_short_name(
    client: AsyncClient, create_user, create_default_url, authorization_header
):
    """
    Trying to update url with invalid slug
    """
    response = await client.patch(
        f"/urls/{create_default_url['short_name']}",
        json={"short_name": "invalid_slug"},
        headers=authorization_header,
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Not valid slug"


@pytest.mark.asyncio
async def test_update_url_invalid_full_name(
    client: AsyncClient, create_user, create_default_url, authorization_header
):
    """
    Trying to update url with invalid url
    """
    response = await client.patch(
        f"/urls/{create_default_url['short_name']}",
        json={"full_name": "invalid_url"},
        headers=authorization_header,
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Not valid url"


@pytest.mark.asyncio
async def test_update_url_occupied_short_name(
    client: AsyncClient, create_user, create_custom_url, authorization_header
):
    """
    Trying to update url with occupied slug
    """
    await client.post(
        f"/urls/custom",
        json={"short_name": "short-name", "full_name": "https://example.com"},
        headers=authorization_header,
    )
    response = await client.patch(
        "/urls/short-name",
        json={"short_name": f"{create_custom_url['short_name']}"},
        headers=authorization_header,
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Url occupied"
