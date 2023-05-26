"""
Module DocString
"""

import json
import os

import requests
from dotenv import load_dotenv

from db.repository import PostgresDB
from grafana.exceptions import GrafanaAPIError, JsonError, NoDataSourceError


class Grafana:
    """
    Class DocString
    """

    API_DATASOURCES = "/api/datasources"
    API_DASHBOARDS = "/api/dashboards/db"
    API_KEYS = "/api/auth/keys"

    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        host: str = "localhost",
        port: str = "3000",
        env_path: str = "./grafana/.env.local.grafana",
    ):
        if user is None or password is None:
            load_dotenv(dotenv_path=env_path)
            self.user = os.environ["GF_SECURITY_ADMIN_USER"]
            self.password = os.environ["GF_SECURITY_ADMIN_PASSWORD"]
        self.api_key = api_key
        self.host = host
        self.port = port

    @property
    def grafana_url(self):
        """
        Method DocString
        """
        return f"http://{self.user}:{self.password}@{self.host}:{self.port}"

    @property
    def headers(self):
        if self.api_key is None:
            raise GrafanaAPIError

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def create_api_key(self):
        """
        Method DocString
        """
        print(f"Creating API KEY with {self.API_KEYS}")
        auth_data = {"Name": self.user, "Role": "Admin", "Password": self.password}
        response = requests.post(
            f"{self.grafana_url+self.API_KEYS}", json=auth_data, timeout=2
        )
        if response.status_code == 200:
            print("API Key successfully created.")
            self.api_key = response.json()["key"]
            print("Writing API Key to file.")
            with open("./grafana/.env.local.grafana_api", mode="w+", encoding="utf-8") as file:
                file.write(self.api_key)
        elif response.status_code == 409:
            print("API Key already exists! Fetching existing API Key.")
            with open("./grafana/.env.local.grafana_api", mode="r+", encoding="utf-8") as file:
                self.api_key = file.readline()
        else:
            print(response.content)

    def add_database_source(self, database: PostgresDB):
        """
        Method DocString
        """

        jsonData = {
            "tlsAuth": False,
            "connMaxLifetime": 14400,
            "database": database.config.database,
            "maxIdleConns": 100,
            "maxIdleConnsAuto": True,
            "maxOpenConns": 100,
            "sslmode": "disable",
            "postgresVersion": 1500,
        }
        secureJsonData = {
            "password": database.config.password,
        }

        datasource = {
            "name": f"{database.type}Python",
            "type": database.type,  # "postgres",
            "url": f"{database.config.host}:{database.config.port}",
            "user": database.config.user,
            "database": database.config.database,
            "basicAuth": False,
            "access": "proxy",
            "withCredentials": False,
            "isDefault": True,
            "jsonData": jsonData,
            "secureJsonData": secureJsonData,
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        print(json.dumps(datasource))
        print()
        response = requests.post(
            self.grafana_url + self.API_DATASOURCES,
            json=datasource,  # json.dumps(datasource),
            headers=headers,
            timeout=2,
        )

        if response.status_code == 200:
            print(
                """
                Data Source Creation of PostgreSQL was successfull.
                """
            )
            response_content = response.json()
            database.datasource_settings = response_content["datasource"]
        elif response.status_code == 409:  # this key has already been created
            print(
                """
                Data Source Creation of PostgreSQL already exists
                """
            )
        else:
            print(response.json())

    def get_all_datasources_info(self) -> list[dict] | None:
        response = requests.get(
            self.grafana_url + self.API_DATASOURCES,
            headers=self.headers,
            timeout=2,
        )
        if response == []:
            raise NoDataSourceError
        if response.status_code == 200:
            print("\nData Source info fetching of PostgreSQL was successfull.")
            return response.json()
        print(response.json())

    def fill_missing_datasource_settings(self, database: PostgresDB) -> None:
        """
        This will find data on an already created datasource associated to the database,
        and fill in the missing information in the database object
        """
        all_info = self.get_all_datasources_info()
        if all_info is not None:
            matching_results = [
                datasource
                for datasource in all_info
                if datasource["name"] == f"{database.type}Python"
            ]
            database.datasource_settings = matching_results[0]

    def upload_to_grafana(self, database: PostgresDB, json_content: dict | None = None):
        """
        Upload dashboard, through a json file,  to grafana and prints response.
        If no json is provided, we just use `grafana_dashboard.json`

        :param json - dashboard json generated by grafanalib
        """
        if json_content is None:
            with open("grafana/grafana_dashboard.json") as json_file:
                json_content = json.load(json_file)
        if json_content is None:
            raise JsonError
        if database.datasource_settings == {}:
            self.fill_missing_datasource_settings(database)
        json_content["panels"][0]["datasource"] = f"{database.type}Python"

        payload = {"dashboard": json_content, "folderId": 0, "overwrite": False}

        response = requests.post(
            self.grafana_url + self.API_DASHBOARDS,
            data=json.dumps(payload),
            headers=self.headers,
            timeout=2,
        )
        if response.status_code == 200:
            print(
                """
                Dashboard creation was successfull.
                """
            )
        else:
            print(response.json())


if __name__ == "__main__":
    from db.db_orm import Base, database_gen, engine
    from db.db_utils import stream_mocker

    grafana = Grafana()
    grafana.create_api_key()
    postgres_db = PostgresDB(filename="./db/database.ini", section="postgresql")
    # grafana.add_database_source(postgres_db)
    # get_initial_db = next(database_gen())
    # result = stream_mocker(Base, engine, get_initial_db)
    # grafana.get_all_datasources_info()
    grafana.upload_to_grafana(postgres_db)
    print("ola")
