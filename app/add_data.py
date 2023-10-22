"""
This module will be responsible for mimicking a
"""

import asyncio

from db import schemas
from db.db_orm import database_gen, engine
from db.db_utils import init_db, stream_mocker

#####################    Creating some initial data in Postgres db    #######################
print(f"Creating tables in {schemas.Base}")
# Base.metadate.create_all should be always in the main.py, from where we run the app.
schemas.Base.metadata.create_all(bind=engine, checkfirst=True)
get_initial_db = next(database_gen())
if get_initial_db.query(schemas.Post).all() == []:
    init_db(schemas.Base, engine, get_initial_db)

# #####################      Simulating a stream of posts    ##################################
asyncio.create_task(stream_mocker(get_initial_db))
