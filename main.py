"""
Module Docstring
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, status
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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    """
    function docstring
    """
    incoming_post = payload.dict()
    incoming_post["id"] = myposts[len(myposts) - 1]["id"] + 1
    myposts.append(incoming_post)
    print(f"Length of myposts: {incoming_post['id']}")
    return incoming_post


@app.get("/posts/latest")
def get_latest_post():
    """
    function docstring
    """
    return {"latest": myposts[len(myposts) - 1]}


@app.get("/posts/{identifier}")
def get_post(identifier: int):
    """
    function docstring
    """
    post_wanted = [post for post in myposts if post["id"] == identifier]
    print(post_wanted)
    if post_wanted == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    # response.status_code = status.HTTP_404_NOT_FOUND
    return {"fetched_post": post_wanted[0]}


@app.delete("/posts/{identifier}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(identifier: int):
    """
    function docstring
    """
    post_wanted = [post for post in myposts if post["id"] == identifier]
    if post_wanted != []:
        myposts.remove(post_wanted[0])


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
