import pytest
from fastapi.testclient import TestClient

from db.schemas import Post as Post_SQL
from pydantic_models.posts import PostResponse


def test_get_all_posts(mock_authorized_client: TestClient, mock_posts: list[Post_SQL]):
    res = mock_authorized_client.get("/posts/")

    def validate(post):
        return PostResponse(**post)

    # validating posts
    [validate(tup["post"]) for tup in res.json()]
    assert len(res.json()) == 3  # only 3 posts were created by mock_user, 1 was by mock_user_2
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(mock_client: TestClient, mock_posts: list[Post_SQL]):
    res = mock_client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(mock_client: TestClient, mock_posts: list[Post_SQL]):
    res = mock_client.get(f"/posts/{mock_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(
    mock_authorized_client: TestClient, mock_posts: list[Post_SQL]
):
    res = mock_authorized_client.get("/posts/88888")
    assert res.status_code == 404


def test_get_one_post(mock_authorized_client: TestClient, mock_posts: list[Post_SQL]):
    res = mock_authorized_client.get(f"/posts/{mock_posts[0].id}")
    post = PostResponse(**res.json())
    assert post.id == mock_posts[0].id
    assert post.content == mock_posts[0].content
    assert post.title == mock_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", True),
    ],
)
def test_create_post(
    mock_authorized_client: TestClient,
    mock_user,
    mock_posts: list[Post_SQL],
    title,
    content,
    published,
):
    res = mock_authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published,
            "username": mock_user["username"],
        },
    )

    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user.id == mock_user["id"]


# def test_create_post_default_published_true(mock_authorized_client, test_user, mock_posts):
#     res = mock_authorized_client.post(
#         "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

#     created_post = schemas.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.title == "arbitrary title"
#     assert created_post.content == "aasdfjasdf"
#     assert created_post.published == True
#     assert created_post.owner_id == test_user['id']


# def test_unauthorized_user_create_post(client, test_user, mock_posts):
#     res = client.post(
#         "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
#     assert res.status_code == 401


# def test_unauthorized_user_delete_Post(client, test_user, mock_posts):
#     res = client.delete(
#         f"/posts/{mock_posts[0].id}")
#     assert res.status_code == 401


# def test_delete_post_success(mock_authorized_client, test_user, mock_posts):
#     res = mock_authorized_client.delete(
#         f"/posts/{mock_posts[0].id}")

#     assert res.status_code == 204


# def test_delete_post_non_exist(mock_authorized_client, test_user, mock_posts):
#     res = mock_authorized_client.delete(
#         f"/posts/8000000")

#     assert res.status_code == 404


# def test_delete_other_user_post(mock_authorized_client, test_user, mock_posts):
#     res = mock_authorized_client.delete(
#         f"/posts/{mock_posts[3].id}")
#     assert res.status_code == 403


# def test_update_post(mock_authorized_client, test_user, mock_posts):
#     data = {
#         "title": "updated title",
#         "content": "updatd content",
#         "id": mock_posts[0].id

#     }
#     res = mock_authorized_client.put(f"/posts/{mock_posts[0].id}", json=data)
#     updated_post = schemas.Post(**res.json())
#     assert res.status_code == 200
#     assert updated_post.title == data['title']
#     assert updated_post.content == data['content']


# def test_update_other_user_post(mock_authorized_client, test_user, test_user2, mock_posts):
#     data = {
#         "title": "updated title",
#         "content": "updatd content",
#         "id": mock_posts[3].id

#     }
#     res = mock_authorized_client.put(f"/posts/{mock_posts[3].id}", json=data)
#     assert res.status_code == 403


# def test_unauthorized_user_update_post(client, test_user, mock_posts):
#     res = client.put(
#         f"/posts/{mock_posts[0].id}")
#     assert res.status_code == 401


# def test_update_post_non_exist(mock_authorized_client, test_user, mock_posts):
#     data = {
#         "title": "updated title",
#         "content": "updatd content",
#         "id": mock_posts[3].id

#     }
#     res = mock_authorized_client.put(
#         f"/posts/8000000", json=data)

#     assert res.status_code == 404
