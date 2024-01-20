import asyncio
from contextlib import ExitStack
import pytest_asyncio
from src import init_app
from src.db import get_db, session_manager
from httpx import AsyncClient
from pytest_postgresql import factories as pg_factories
from pytest_postgresql.janitor import DatabaseJanitor


user_data = {"username": "username", "password": "password"}


@pytest_asyncio.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


test_db = pg_factories.postgresql_proc(dbname="test_db", port=None)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_dbname = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_dbname, test_db.version, pg_password
    ):
        test_db_url = f"postgresql+asyncpg://{pg_user}:@{pg_host}:{pg_port}/{pg_dbname}"
        session_manager.init(test_db_url)
        yield
        await session_manager.close()


@pytest_asyncio.fixture(autouse=True)
async def create_tables(connection_test):
    async with session_manager.connect() as connection:
        await session_manager.drop_all(connection)
        await session_manager.create_all(connection)


@pytest_asyncio.fixture(autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with session_manager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


@pytest_asyncio.fixture
async def create_user(client: AsyncClient):
    response = await client.post("/users", json=user_data)
    return response.json()


@pytest_asyncio.fixture
async def authorize(client: AsyncClient):
    response = await client.post("/auth/login", json=user_data)
    tokens = response.json()
    return tokens


@pytest_asyncio.fixture
async def authorization_header(authorize):
    return {"Authorization": f'Bearer {authorize["access_token"]}'}
