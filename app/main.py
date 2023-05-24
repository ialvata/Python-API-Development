"""
Module Docstring
"""

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import db.models
import db.schemas
from db.db_orm import Base, engine, get_database
from db.db_utils import init_db
from grafana.grafana_utils import Grafana
from db.repository import PostgresDB

#####################    Creating some initial data in Postgres db    #######################
Base.metadata.create_all(bind=engine)
get_initial_db = next(get_database())
if get_initial_db.query(db.schemas.Post).all() == []:
    init_db(Base, engine, get_initial_db)

#####################    Adding a Postgres db datasource to Grafana     #######################

grafana = Grafana()
grafana.create_api_key()
postgres_db = PostgresDB(filename="./db/database.ini", section="postgresql")
grafana.add_database_source(postgres_db)


##############################    Creatng FastAPI App   ##########################
app = FastAPI()
 
print()


@app.get("/")
async def root():
    """
    function docstring
    """
    return {"message": "Hello World 2"}


@app.get("/posts")
def get_all_posts(db_session: Session = Depends(get_database)):
    """
    function docstring
    """
    posts = db_session.query(db.schemas.Post).all()
    # .execute("SELECT * FROM posts")
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: db.models.Post, db_session: Session = Depends(get_database)):
    """
    function docstring
    """
    # creating a data according to schema
    new_post = db.schemas.Post(**(payload.dict()))
    # adding data to session, moving it to pending state.
    db_session.add(new_post)
    # moving all data in pending state, in this session, to persistant state.
    db_session.commit()
    # update new_post with data returned from db_session
    db_session.refresh(new_post)
    return {"data": new_post}


# path operations are evaluated in order,
# you need to make sure that the path for /posts/latest
# is declared before the one for /posts/{identifier}
# @app.get("/posts/latest")
# def get_latest_post(db_session: Session = Depends(get_database)):
#     """
#     function docstring
#     """
#     return {"latest": myposts[len(myposts) - 1]}


# identifier is an example of a path parameter
# we could also
@app.get("/posts/{identifier}")
def get_post(identifier: int, db_session: Session = Depends(get_database)):
    """
    Creates endpoint to fetch specific post
    """
    post_wanted = (
        db_session.query(db.schemas.Post).where(db.schemas.Post.id == identifier).first()
    )
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    # response.status_code = status.HTTP_404_NOT_FOUND
    return {"fetched_post": post_wanted}


# here identifier is a Query parameter
@app.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(identifier: int, db_session: Session = Depends(get_database)):
    """
    Function that creates the resource to delete a specified post, by identifier.
    """
    post_wanted = (
        db_session.query(db.schemas.Post).where(db.schemas.Post.id == identifier).first()
    )
    if post_wanted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    db_session.delete(post_wanted)
    db_session.commit()


@app.patch("/posts/{identifier}", status_code=status.HTTP_200_OK)
def patch_post(
    identifier: int, payload: db.models.Post, db_session: Session = Depends(get_database)
):
    """
    function docstring
    """
    post_wanted = db_session.query(db.schemas.Post).where(db.schemas.Post.id == identifier)
    if post_wanted.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {identifier} not found!",
        )
    # pylance type checker says that payload.dict() is incompatible with type of `values` from
    # update... hence the extra dict()
    post_wanted.update(dict(payload.dict()), synchronize_session=False)
    db_session.commit()
    return {"fetched_post": post_wanted.first()}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
