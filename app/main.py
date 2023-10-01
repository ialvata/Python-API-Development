"""
Module Docstring
"""

import asyncio

import uvicorn
from fastapi import FastAPI

from app.routers import auth, posts, users, votes
from db import schemas
from db.db_orm import database_gen, engine
from db.db_utils import init_db, stream_mocker
from db.repository import PostgresDB
from grafana.grafana_utils import Grafana
from prometheus.prometheus_utils import PrometheusDB

#####################    Creating some initial data in Postgres db    #######################
print(f"Creating tables in {schemas.Base}")
# Base.metadate.create_all should be always in the main.py, from where we run the app.
schemas.Base.metadata.create_all(bind=engine, checkfirst=True)
get_initial_db = next(database_gen())
if get_initial_db.query(schemas.Post).all() == []:
    init_db(schemas.Base, engine, get_initial_db)

#####################    Adding a Postgres db datasource to Grafana     #######################
grafana = Grafana()
grafana.create_api_key()
postgres_db = PostgresDB(filename="./db/database.ini", section="postgresql")
grafana.add_database_source(postgres_db)
grafana.upload_to_grafana(postgres_db)
prometheus_db = PrometheusDB(filename="./prometheus/config.ini", section="prometheus")

grafana.add_prometheus_source(prometheus_db)
print(grafana.get_all_datasources_info())
#####################      Simulating a stream of posts    ##################################
asyncio.create_task(stream_mocker(get_initial_db))

##############################    Creatng FastAPI App   ##########################
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    """
    function docstring
    """
    return {"message": "Hello World 2"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
