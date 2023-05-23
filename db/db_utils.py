"""
Module with all the boilerplate code to start a SQLAlchemy session in the PostgreSQL DB
"""

from sqlalchemy import Engine

from db.models import Post as Post_pydantic
from db.schemas import Post as Post_sql


def init_db(base, engine: Engine, db_session):
    """
    Function to create some initial data in the DB
    """
    base.metadata.create_all(bind=engine)
    ##########################    cached posts   ##########################
    myposts = [
        Post_pydantic(title=f"title_{idx}", content=f"content_{idx}") for idx in range(1, 11)
    ]
    for post in myposts:
        db_session.add(Post_sql(**(post.dict())))
    db_session.commit()

    print("Initialized the db")
