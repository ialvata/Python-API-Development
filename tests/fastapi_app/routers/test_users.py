"""
This module will include tests for all the basic crud operations.
"""

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from authetication.oauth2 import ALGORITHM, SECRET_KEY, Token
from pydantic_models.users import UserResponse


def test_create_user(mock_client: TestClient):
    res = mock_client.post(
        "/users/",
        json={"email": "hello123@gmail.com", "password": "password123", "username": "Jonas"},
    )
    print("res -> ", res.content)
    new_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello123@gmail.com"
    assert new_user.username == "Jonas"


def test_login_user(mock_user: dict, mock_client: TestClient):
    res = mock_client.post(
        "/login", data={"username": mock_user["username"], "password": mock_user["password"]}
    )
    print(res.content)
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("username")
    assert id == mock_user["username"]
    assert login_res.token_type == "Bearer"
    assert res.status_code == 202


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("sanjeev@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(
    mock_user: dict, mock_client: TestClient, email: str, password: str, status_code: int
):
    # mock_user is not accessed, but it's a fixture used to initialize the db in conftest.py
    res = mock_client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
