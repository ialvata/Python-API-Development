import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.main import app
from authetication.oauth2 import create_access_token
from db.db_orm import PostgresCredentials, database_gen
from db.schemas import Base, Post

test_pg_cred = PostgresCredentials("./db/.env.test.db")
TEST_POSTGRES_DB_URL = (
    f"postgresql://{test_pg_cred.postgres_user}:"
    f"{test_pg_cred.postgres_password}@localhost/{test_pg_cred.postgres_database_name}"
)
engine = create_engine(TEST_POSTGRES_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("Creating a Test Database Session")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session: Session):
    # we're using the session fixture defined above
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database_gen] = override_get_db
    yield TestClient(app)


@pytest.fixture
def mock_user2(client: TestClient):
    # We're using the client fxture defined above
    user_data = {"email": "sanjeev123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def mock_user(client: TestClient):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(mock_user):
    return create_access_token({"user_id": mock_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(mock_user, session: Session, test_user2):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": mock_user["id"]},
        {"title": "2nd title", "content": "2nd content", "owner_id": mock_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": mock_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user2["id"]},
    ]

    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()
    return posts
