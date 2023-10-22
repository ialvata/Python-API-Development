import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.main import app
from authetication.oauth2 import create_access_token
from db.db_orm import PostgresCredentials, database_gen
from db.schemas import Base, Post

test_pg_cred = PostgresCredentials(path="./db/.env.test.db")
TEST_POSTGRES_DB_URL = (
    f"postgresql://{test_pg_cred.postgres_user}:"
    f"{test_pg_cred.postgres_password}@localhost:"
    f"{test_pg_cred.postgres_port}/{test_pg_cred.postgres_database_name}"
)
engine = create_engine(TEST_POSTGRES_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def mock_session():
    print("Creating a Test Database Session")
    Base.metadata.drop_all(bind=engine)  # restart a clean new database
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def mock_client(mock_session: Session):
    # we're using the session fixture defined above
    def override_get_db():
        try:
            yield mock_session
        finally:
            mock_session.close()

    app.dependency_overrides[database_gen] = override_get_db
    yield TestClient(app)


@pytest.fixture
def mock_user2(mock_client: TestClient) -> dict:
    # We're using the client fxture defined above
    user_data = {
        "username": "Jonas123",
        "email": "sanjeev123@gmail.com",
        "password": "password123",
    }
    res = mock_client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def mock_user(mock_client: TestClient) -> dict:
    user_data = {"username": "Jonas", "email": "sanjeev@gmail.com", "password": "password123"}
    res = mock_client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def mock_token(mock_user: dict):
    return create_access_token({"username": mock_user["username"]})


@pytest.fixture
def mock_authorized_client(mock_client: TestClient, mock_token: str):
    mock_client.headers = {**mock_client.headers, "authorization": f"Bearer {mock_token}"}
    return mock_client


@pytest.fixture
def mock_posts(mock_user: dict, mock_session: Session, mock_user2: dict):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "username": mock_user["username"],
        },
        {"title": "2nd title", "content": "2nd content", "username": mock_user["username"]},
        {"title": "3rd title", "content": "3rd content", "username": mock_user["username"]},
        {"title": "3rd title", "content": "3rd content", "username": mock_user2["username"]},
    ]

    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    mock_session.add_all(posts)
    mock_session.commit()
    posts = mock_session.query(Post).all()
    return posts
