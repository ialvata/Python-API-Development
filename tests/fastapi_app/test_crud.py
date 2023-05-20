"""
This module will include tests for all the basic crud operations.
"""
import os

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app, myposts

print(os.getcwd())

client = TestClient(app)


def test_root():
    """
    testing root resource
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World 2"}


def test_get_all_posts():
    """
    testing get_all_posts resource
    """
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == {"data": myposts}


@pytest.mark.parametrize(
    "identifier",
    [
        # the first
        (0),
        (len(myposts)),
    ],
)
def test_get_post(identifier: int):
    """
    testing get_post resource
    """
    response = client.get(f"/posts/{identifier}")
    print(identifier)

    if identifier < len(myposts):
        assert response.status_code == 200
        assert response.json() == {"fetched_post": myposts[identifier]}
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": f"Post with id {identifier} not found!"}

    # post_wanted = find_post(identifier)
    # print(post_wanted)
    # if post_wanted is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id {identifier} not found!",
    #     )
    # # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"fetched_post": post_wanted[0]}
