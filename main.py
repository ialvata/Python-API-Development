"""
Module Docstring
"""

from fastapi import FastAPI
from pydantic import BaseModel


class Body(BaseModel):
    """
    Class docstring
    """

    title: str
    content: str | None = None


app = FastAPI()


@app.get("/")
async def root():
    """
    function docstring
    """
    return {"message": "Hello World 2"}


@app.get("/posts")
def get_posts():
    """
    function docstring
    """
    return {"data": "This is your post"}


@app.post("/post_posts")
def post_posts(payload: Body):
    """
    function docstring
    """
    print(f"Title: {payload.title}")
    return payload
