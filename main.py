"""
Module Docstring
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Post(BaseModel):
    """
    Class docstring
    """

    title: str
    content: str | None = None
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()


myposts = [Post(title=f"title_{idx}", content=f"content_{idx}").dict() for idx in range(10)]
for post, idx in zip(myposts, range(len(myposts))):
    post.update({"id": idx})


@app.get("/")
async def root():
    """
    function docstring
    """
    return {"message": "Hello World 2"}


@app.get("/posts")
def get_all_posts():
    """
    function docstring
    """
    return {"data": myposts}


@app.post("/posts")
def create_post(payload: Post):
    """
    function docstring
    """
    incoming_post = payload.dict()
    incoming_post["id"] = len(myposts)
    myposts.append(incoming_post)
    print(f"Length of myposts: {incoming_post['id']}")
    return post


@app.get("/posts/{identifier}")
def get_post(identifier):
    """
    function docstring
    """
    post_wanted = [post for post in myposts if post["id"] == int(identifier)]
    print(post_wanted)
    return {"fetched_post": post_wanted}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
