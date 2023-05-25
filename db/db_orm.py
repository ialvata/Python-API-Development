"""
Module with all the boilerplate code to start a SQLAlchemy session in the PostgreSQL DB
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path="./db/.env.local.db")

postgres_user = os.environ["POSTGRES_USER"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_database_name = os.environ["POSTGRES_DB"]

POSTGRESQL_DATABASE_URL = (
    f"""postgresql://{postgres_user}:{postgres_password}@localhost/{postgres_database_name}"""
)

engine = create_engine(POSTGRESQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def database_gen():
    """
    Function responsible for yielding a session and closing it.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
