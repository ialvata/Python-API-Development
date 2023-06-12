"""
Module Docstring
"""

import uvicorn
from fastapi import FastAPI

from app.routers import auth, posts, users
from db import schemas
from db.db_orm import Base, database_gen, engine
from db.db_utils import init_db  # , stream_mocker
from db.repository import PostgresDB
from grafana.grafana_utils import Grafana

#####################    Creating some initial data in Postgres db    #######################
print(f"Creating tables in {Base}")
# Base.metadate.create_all should be always in the main.py, from where we run the app.
Base.metadata.create_all(bind=engine, checkfirst=True)
get_initial_db = next(database_gen())
if get_initial_db.query(schemas.Post).all() == []:
    init_db(Base, engine, get_initial_db)

#####################    Adding a Postgres db datasource to Grafana     #######################
grafana = Grafana()
grafana.create_api_key()
postgres_db = PostgresDB(filename="./db/database.ini", section="postgresql")
grafana.add_database_source(postgres_db)
grafana.upload_to_grafana(postgres_db)


#####################      Simulating a stream of posts    ##################################
# stream_mocker(get_initial_db)

##############################    Creatng FastAPI App   ##########################
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """
    function docstring
    """
    return {"message": "Hello World 2"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
