"""
Module with all the boilerplate code to start a SQLAlchemy session in the PostgreSQL DB
"""
from random import uniform
from time import sleep

from sqlalchemy import Engine

from db.models import Post as Post_pydantic
from db.schemas import Post as Post_sql


def init_db(base, engine: Engine, db_session):
    """
    Function to create some initial data in the DB
    """
    print("Creating posts table")
    base.metadata.create_all(bind=engine)
    ##########################    cached posts   ##########################
    print("Creating cached posts")
    myposts = [
        Post_pydantic(title=f"title_{idx}", content=f"content_{idx}", rating=uniform(0, idx))
        for idx in range(1, 10)
    ]
    print("Adding posts and commiting them")
    for index, post in enumerate(myposts):
        sleep(uniform(0, 1))
        print(f"Post with index ->{index}")
        db_session.add(Post_sql(**(post.dict())))
        db_session.commit()

    print("Initialized the db")


def stream_mocker(base, engine: Engine, db_session):
    """
    Function to create some initial data in the DB
    """
    print("Creating posts table")
    base.metadata.create_all(bind=engine)
    ##########################    cached posts   ##########################
    print("Creating cached posts")
    myposts = [
        Post_pydantic(title=f"title_{idx}", content=f"content_{idx}", rating=uniform(0, 100))
        for idx in range(1, 1100)
    ]
    print("Adding posts and commiting them")
    for index, post in enumerate(myposts):
        sleep(uniform(0, 5))
        print(f"Post with index ->{index}")
        db_session.add(Post_sql(**(post.dict())))
        db_session.commit()

    print("Initialized the db")
