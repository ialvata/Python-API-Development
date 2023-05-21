"""
This module is responsible for defining everything related to databases.
I would usually separate into different modules the parent class from the subclasses, but in
this situation the number of code lines is too few to justify it...
"""
from configparser import ConfigParser
from typing import Optional, Protocol, runtime_checkable

import psycopg2
from psycopg2._psycopg import cursor  # pylint: disable = no-name-in-module
from pydantic import BaseModel

from db.utils import ConfigEmptyError, ConfigFormatError


class ConfigDB(BaseModel):
    """
    class representing the configuration for the db.
    """

    host: str | None = None
    database: str | int | None = None
    user: str | None = None
    password: str | None = None


@runtime_checkable
class DataBase(Protocol):
    """
    Super class for all database classes
    """

    def __init__(
        self,
        config: ConfigDB,
        filename: str | None = None,
        section: str | None = None,
    ):
        """method docstring"""

    def connect(self):
        """method docstring"""

    def create_table(self):
        """method docstring"""


class PostgresDB:
    """
    Class responsible for all the operations on the Postgres database.
    It will try to be hide all the implementation details of the Postgres db.
    """

    def __init__(
        self,
        config: ConfigDB | None = None,
        filename: str | None = None,
        section: str | None = None,
    ):
        """method docstring"""
        self.filename = filename
        self.section = section
        if self.filename is not None and self.section is not None:
            # create a parser
            parser = ConfigParser()
            # read config file
            parser.read(self.filename)

            # get section, default to postgresql
            config_dict = {}
            if parser.has_section(self.section):
                params = parser.items(self.section)
                for param in params:
                    config_dict[param[0]] = param[1]
            else:
                raise ConfigFormatError(section=self.section, filename=self.filename)
            config_dict: dict[str, str]
            self.config = ConfigDB(**config_dict)
        if config is not None:
            self.config = config
        if not hasattr(self, "config"):
            raise ConfigEmptyError

    def connect(self) -> Optional[cursor]:
        """Connect to the PostgreSQL database server"""
        conn = None
        try:
            # connect to the PostgreSQL server
            print("Connecting to the PostgreSQL database...")
            conn = psycopg2.connect(**self.config.dict())
            # create a cursor
            cur = conn.cursor()
            if cur:
                return cur
            return None
        except psycopg2.DatabaseError as error:
            print(error)
            return None

    def create_table(self):
        """method docstring"""


if __name__ == "__main__":
    db = PostgresDB(filename="./db/database.ini", section="postgresql")
    print(isinstance(db, DataBase))  # True
    # db = PostgresDB(filename="Asdasd") # raises error
