"""
Module Docstring
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from db.database import Base, SessionLocal, engine
from db.repository import PostgresDB


class Post(BaseModel):
    """
    Class docstring
    """

    title: str
    content: str | None = None
    published: bool = True
    rating: Optional[int] = None


##########################    cached posts   ##########################
myposts = [Post(title=f"title_{idx}", content=f"content_{idx}").dict() for idx in range(1, 11)]
for post, idx in zip(myposts, range(len(myposts))):
    post.update({"id": idx})

##########################    connecting to Postgres db    ##########################
database = PostgresDB(filename="./db/database.ini", section="postgresql")
database.connect()

#####################    creating some initial data in Postgres db    #######################
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


database.execute(
    """
    CREATE TABLE posts (
        id serial PRIMARY KEY,
        title varchar NOT NULL,
        content varchar,
        published boolean DEFAULT true,
        created_at TIMESTAMP
    );
    """
)
for post in myposts:
    database.execute(
        # pylint: disable = f-string-without-interpolation
        f"""
        INSERT INTO posts (title, content,published)
        VALUES (%s,%s,%s)
        """,
        (post["title"], post["content"], post["published"]),
    )


##############################    Creatng FastAPI App   ##########################
app = FastAPI()


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
    database.execute("SELECT * FROM posts")
    posts = database.get_all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    """
    function docstring
    """
    database.execute(
        # pylint: disable = f-string-without-interpolation
        f"""
        INSERT INTO posts (title, content,published)
        VALUES (%s,%s,%s)
        """,
        (payload.title, str(payload.content), str(payload.published)),
    )
    new_post = database.get_all()

    return {"data": new_post}


# path operations are evaluated in order,
# you need to make sure that the path for /posts/latest
# is declared before the one for /posts/{identifier}
@app.get("/posts/latest")
def get_latest_post():
    """
    function docstring
    """
    return {"latest": myposts[len(myposts) - 1]}


def find_post(identifier: int) -> dict | None:
    """
    function docstring
    """
    list_res = [post for post in myposts if post["id"] == identifier]
    if list_res == []:
        return None
    return list_res[0]


# identifier is an example of a path parameter
# we could also
@app.get("/posts/{identifier}")
def get_post(identifier: int):
    """
    function docstring
    """
    post_wanted = find_post(identifier)
    print(post_wanted)
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    # response.status_code = status.HTTP_404_NOT_FOUND
    return {"fetched_post": post_wanted}


# here identifier is a Query parameter
@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(identifier: int):
    """
    function docstring
    """
    post_wanted = find_post(identifier)
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    myposts.remove(post_wanted)


@app.patch("/posts/{identifier}", status_code=status.HTTP_200_OK)
def patch_post(identifier: int, payload: Post):
    """
    function docstring
    """
    post_wanted = find_post(identifier)
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    post_wanted.update(payload)
    return {"fetched_post": post_wanted}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
