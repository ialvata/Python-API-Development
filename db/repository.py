"""
This module is responsible for defining everything related to databases.
I would usually separate into different modules the parent class from the subclasses, but in
this situation the number of code lines is too few to justify it...
"""
from configparser import ConfigParser
from typing import Protocol, runtime_checkable

import psycopg2
from pydantic import BaseModel

from db.utils import ConfigEmptyError, ConfigFormatError, ConnectFirstError, CursorNoneError


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

    def execute(self, sql_command: str, values: tuple[str, ...] | None = None):
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
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the PostgreSQL database server"""
        try:
            # connect to the PostgreSQL server
            print("Connecting to the PostgreSQL database...")
            self.conn = psycopg2.connect(**self.config.dict())
            # create a cursor
            print("Setting Cursor...")
            cursor = self.conn.cursor()
            if cursor:
                self.cursor = cursor
            else:
                raise CursorNoneError
        except psycopg2.DatabaseError as error:
            print(error)
            raise error

    def execute(self, sql_command: str, values: tuple[str, ...] | None = None):
        """method docstring"""
        if self.cursor is not None and self.conn is not None:
            self.cursor.execute(sql_command, values)
            self.conn.commit()
        raise ConnectFirstError

    def get_all(self):
        """method docstring"""
        if self.cursor is not None:
            return self.cursor.fetchall()
        raise ConnectFirstError


if __name__ == "__main__":
    db = PostgresDB(filename="./db/database.ini", section="postgresql")
    print(isinstance(db, DataBase))  # True
    # db = PostgresDB(filename="Asdasd") # raises error
    db.connect()
