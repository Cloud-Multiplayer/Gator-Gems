import pytest

from sqlmodel import StaticPool, create_engine, Session

from app.main import app
from fastapi.testclient import TestClient

from app.database.connections import get_session
from app.database.schema import create_db_and_tables
from app.models.users import User
from tests.mocks.users import MOCK_USER


@pytest.fixture(name="session", scope="function")
def session_fixture():
    test_engine = create_engine(
        "sqlite://",  # In-memory SQLite database
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    create_db_and_tables(test_engine)

    with Session(test_engine) as session:
        yield session

    test_engine.dispose()


@pytest.fixture(name="client", scope="function")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user", scope="function")
def user_fixture():
    yield User(**MOCK_USER.model_dump())  # Create a new User instance for each test
