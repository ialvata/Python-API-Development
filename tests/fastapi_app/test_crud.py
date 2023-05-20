"""
This module will include tests for all the basic crud operations.
"""
from fastapi.testclient import TestClient

from app.main import app, myposts

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
