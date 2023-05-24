"""
Module DocString
"""

import os

import requests
from dotenv import load_dotenv

from db.repository import PostgresDB


class Grafana:
    """
    Class DocString
    """
    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        host: str = "localhost",
        port: str = "3000",
        API_DATASOURCES:str = "/api/datasources",
        API_KEYS:str = "/api/auth/keys",
        env_path:str = "./grafana/.env.local.grafana",
    ):
        if user is None or password is None:
            load_dotenv(dotenv_path = env_path)
            self.user = os.environ["GF_SECURITY_ADMIN_USER"]
            self.password = os.environ["GF_SECURITY_ADMIN_PASSWORD"]
        self.api_key = api_key
        self.host = host
        self.port = port
        self.API_DATASOURCES = API_DATASOURCES
        self.API_KEYS = API_KEYS
    @property
    def grafana_url(self):
        """
        Method DocString
        """
        return f"http://{self.user}:{self.password}@{self.host}:{self.port}"

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
        datasource = {
            "name": "PostgreSQL",
            "type": "postgres",
            "host": f"http://{database.config.host}",
            "database": database.config.database,
            "user": database.config.user,
            "password": database.config.password,
            "access": "proxy",
            "port" : "6543"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.post(
            self.grafana_url + self.API_DATASOURCES,
            json=datasource,
            headers=headers,
            timeout=2,
        )

        if response.status_code == 200:
            print(
                """
                Data Source Creation of PostgreSQL was successfull.
                """
            )
        elif response.status_code == 409:  # this key has already been created
            print(
                """
                Data Source Creation of PostgreSQL already exists
                """
            )
        else:
            print(response.content)
        # database.connect()
        # database.execute(
        #     """
        #     ALTER ROLE python_api_dev set search_path = "posts";
        #     """
        # )



if __name__ == "__main__":
    
    grafana = Grafana()
    grafana.create_api_key()
    postgres_db = PostgresDB(filename="./db/database.ini", section="postgresql")
    grafana.add_database_source(postgres_db)
