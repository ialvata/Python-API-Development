"""
Module Docstring
"""
import uvicorn
from fastapi import FastAPI

from app.routers import auth, posts, users, votes
from db.repository import PostgresDB
from grafana.grafana_utils import Grafana
from prometheus.prometheus_utils import PrometheusDB

#####################    Adding a Postgres db datasource to Grafana     #######################
grafana = Grafana()
grafana.create_api_key()
postgres_db = PostgresDB(filename="./db/database.ini", section="postgresql")
grafana.add_database_source(postgres_db)
grafana.upload_to_grafana(postgres_db)
#####################      Adding a Prometheus DB to Grafana      #############################
prometheus_db = PrometheusDB(filename="./prometheus/config.ini", section="prometheus")
grafana.add_prometheus_source(prometheus_db)
# print(grafana.get_all_datasources_info())

##############################    Creatng FastAPI App   ##########################
app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
