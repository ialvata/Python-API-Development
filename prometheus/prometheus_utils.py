from configparser import ConfigParser

from pydantic import BaseModel

from db.exceptions import (  # ConnectFirstError,; CursorNoneError,
    ConfigEmptyError,
    ConfigFormatError,
)


class ConfigDB(BaseModel):
    """
    Class representing the configuration for the db.
    """

    host: str = "localhost"
    user: str | None = None
    password: str | None = None
    port: str = "9090"


class PrometheusDB:
    """
    Class responsible for all the operations on the Postgres database.
    It will try to be hide all the implementation details of the Postgres db.
    """

    type = "prometheus"

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
        self.datasource_settings = {}

    # def connect(self):
    #     """
    #     Connect to the PostgreSQL database server

    #     ## Example usage:
    #     database = PostgresDB(filename="./db/database.ini", section="postgresql")
    #     database.connect()

    #     """
    #     try:
    #         # connect to the PostgreSQL server
    #         print("Connecting to the PostgreSQL database...")
    #         self.conn = psycopg2.connect(**self.config.dict())
    #         # create a cursor
    #         print("Setting Cursor...")
    #         cursor = self.conn.cursor()
    #         if cursor:
    #             self.cursor = cursor
    #         else:
    #             raise CursorNoneError
    #     except psycopg2.DatabaseError as error:
    #         print(error)
    #         raise error
