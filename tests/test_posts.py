from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    posts = [schemas.Post(**post) for post in res.json()]

    assert len(posts) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_does_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/10000")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post(**res.json())
    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("title1", "content1", True),
        ("title2", "content2", False),
        ("title3", "content3", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner.id == test_user["id"]

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "title4", "content": "content4"})

    post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post.title == "title4"
    assert post.content == "content4"
    assert post.published == True
    assert post.owner.id == test_user["id"]

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post(
        "/posts/", json={"title": "title4", "content": "content4"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_authorized_user_delete_post_does_not_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/10000")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_posts, test_user):
    data = {"title": "update title", "content": "update content", "published": False}

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user2, test_posts, test_user):
    data = {"title": "update title", "content": "update content", "published": False, "id": test_posts[3].id}

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_user):
    res = client.put(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_authorized_user_update_post_does_not_exist(authorized_client, test_posts, test_user):
    data = {"title": "update title", "content": "update content", "published": False}

    res = authorized_client.put(f"/posts/8000", json=data)
    assert res.status_code == 404
