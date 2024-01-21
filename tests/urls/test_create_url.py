import pytest
from httpx import AsyncClient
from pytest_schema import exact_schema
from .schemas import url
from ..conftest import (
    url_default_data,
    url_custom_data,
    create_user,
    create_default_url,
    create_custom_url,
    authorization_header,
)


@pytest.mark.asyncio
async def test_create_default_url(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create default url
    """
    response = await client.post(
        "/urls/default", json=url_default_data, headers=authorization_header
    )
    assert response.status_code == 201
    assert exact_schema(url) == response.json()
    assert response.json().get("full_name") == url_default_data["full_name"]


@pytest.mark.asyncio
async def test_create_default_url_unauthorized(client: AsyncClient, create_user):
    """
    Trying to create default url unauthorized
    """
    response = await client.post("/urls/default", json=url_default_data)
    assert response.status_code == 401
    assert response.json() != exact_schema(url)


@pytest.mark.asyncio
async def test_create_default_url_blank_body(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create default url with blank body
    """
    response = await client.post("/urls/default", json={}, headers=authorization_header)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invalid_default_url_data(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create default url with invalid body content
    """
    response = await client.post(
        "/urls/default", json={"a": "b"}, headers=authorization_header
    )
    assert response.status_code == 422

    response = await client.post(
        "/urls/default", json={"a": "", "b": ""}, headers=authorization_header
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_default_url_with_invalid_url(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create default url with invalid url
    """
    response = await client.post(
        "/urls/default", json={"full_name": "invalid_url"}, headers=authorization_header
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not valid url"


@pytest.mark.asyncio
async def test_create_existing_default_url(
    client: AsyncClient, create_user, create_default_url, authorization_header
):
    """
    Trying to create existing default url
    """
    response = await client.post(
        "/urls/default", json=url_default_data, headers=authorization_header
    )
    assert response.status_code == 201
    assert exact_schema(url) == response.json()


@pytest.mark.asyncio
async def test_create_custom_url(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create custom url
    """
    response = await client.post(
        "/urls/custom", json=url_custom_data, headers=authorization_header
    )
    assert response.status_code == 201
    assert exact_schema(url) == response.json()
    assert response.json().get("full_name") == url_custom_data["full_name"]
    assert response.json().get("short_name") == url_custom_data["short_name"]


@pytest.mark.asyncio
async def test_create_custom_url_unauthorized(client: AsyncClient, create_user):
    """
    Trying to create custom url unauthorized
    """
    response = await client.post("/urls/custom", json=url_custom_data)
    assert response.status_code == 401
    assert response.json() != exact_schema(url)


@pytest.mark.asyncio
async def test_create_custom_url_blank_body(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create custom url with blank body
    """
    response = await client.post("/urls/custom", json={}, headers=authorization_header)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_invalid_custom_url_data(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create custom url with invalid body content
    """
    response = await client.post(
        "/urls/custom", json={"a": "b"}, headers=authorization_header
    )
    assert response.status_code == 422

    response = await client.post(
        "/urls/custom", json={"a": "", "b": ""}, headers=authorization_header
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_custom_url_with_invalid_url(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create custom url with invalid url
    """
    response = await client.post(
        "/urls/custom",
        json={"full_name": "invalid_url", "short_name": url_custom_data["short_name"]},
        headers=authorization_header,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not valid url"


@pytest.mark.asyncio
async def test_create_custom_url_with_invalid_slug(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to create custom url with invalid slug
    """
    response = await client.post(
        "/urls/custom",
        json={"full_name": url_custom_data["full_name"], "short_name": "invalid_slug"},
        headers=authorization_header,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Not valid slug"


@pytest.mark.asyncio
async def test_create_existing_custom_url(
    client: AsyncClient, create_user, create_custom_url, authorization_header
):
    """
    Trying to create existing custom url
    """
    response = await client.post(
        "/urls/custom", json=url_custom_data, headers=authorization_header
    )
    assert response.status_code == 400
    assert response.json().get("detail") == "Slug already in use"
