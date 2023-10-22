"""
Module with all the boilerplate code to start a SQLAlchemy session in the PostgreSQL DB
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresCredentials:
    def __init__(self, path: str = "./db/.env.local.db") -> None:
        load_dotenv(dotenv_path=path, override=True)
        # we need override for when we do tests, since we initially import the main app, which
        # has a initial dependency on "./db/.env.local.db", so PostgresCredentials is being
        # called twice, instead of just once.
        self.postgres_user = os.environ["POSTGRES_USER"]
        self.postgres_password = os.environ["POSTGRES_PASSWORD"]
        self.postgres_database_name = os.environ["POSTGRES_DB"]
        self.postgres_port = os.environ.get("POSTGRES_PORT", 5432)


pg_cred = PostgresCredentials()
POSTGRESQL_DATABASE_URL = (
    f"postgresql://{pg_cred.postgres_user}:"
    f"{pg_cred.postgres_password}@localhost/{pg_cred.postgres_database_name}"
)


engine = create_engine(POSTGRESQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
