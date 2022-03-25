import os

import sqlalchemy
from sqlalchemy_utils import database_exists, create_database

import services.database.engine


class Engine:
    @staticmethod
    def __get_connection_string():

        user = os.getenv("MARIADB_USER")
        password = os.getenv("MARIADB_PASSWORD")

        uri = os.getenv("MARIADB_URI")
        port = os.getenv("MARIADB_PORT")

        db = os.getenv("MARIADB_DB")

        if not uri:
            uri = "127.0.0.1"

        if not port:
            port = "3306"

        if not db:
            db = "vireo"

        return f"mariadb+mariadbconnector://{user}:{password}@{uri}:{port}/{db}"

    @staticmethod
    def get_engine():
        engine = sqlalchemy.create_engine(services.database.engine.Engine.__get_connection_string())

        if not database_exists(engine.url):
            create_database(engine.url)

        return engine