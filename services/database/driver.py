import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def get_connection_string():
    user = os.getenv("MARIADB_USER")
    password = os.getenv("MARIADB_PASSWORD")

    uri = os.getenv("MARIADB_URI")
    port = os.getenv("MARIADB_PORT")

    db = os.getenv("MARIADB_DB")

    if not db:
        db = "vireo"

    if not uri:
        uri = "127.0.0.1"

    if not port:
        port = "3306"

    return f"mariadb+mariadbconnector://{user}:{password}@{uri}:{port}/{db}"


def get_engine():
    engine = sqlalchemy.create_engine(get_connection_string())

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


class Driver:
    def __init__(self):
        self.engine = get_engine()
        self.session = get_session(self.engine)


driver_service = Driver()
