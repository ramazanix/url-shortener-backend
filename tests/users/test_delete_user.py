import pytest
from httpx import AsyncClient
from ..conftest import user_data


@pytest.mark.asyncio
async def test_delete_current_user_unauthorized(client: AsyncClient, create_user):
    """
    Trying to delete current user without auth
    """
    response = await client.delete(f"/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_current_user_authorized(
    client: AsyncClient, create_user, authorization_header
):
    """
    Trying to delete current user with auth
    """
    response = await client.delete(f"/users/me", headers=authorization_header)
    assert response.status_code == 204
