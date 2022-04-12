import os

import sqlalchemy
from sqlalchemy.exc import PendingRollbackError, OperationalError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from tenacity import stop_after_attempt, wait_exponential, retry


def get_connection_string():
    user = os.getenv("MARIADB_USER", default="root")
    password = os.getenv("MARIADB_PASSWORD", default="root")

    uri = os.getenv("MARIADB_URI", default="127.0.0.1")
    port = os.getenv("MARIADB_PORT", default="3306")

    db = os.getenv("MARIADB_DB", default="vireo")

    return f"mysql+pymysql://{user}:{password}@{uri}:{port}/{db}"


@retry(stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=1, min=1, max=5))
def get_engine():
    engine = sqlalchemy.create_engine(get_connection_string())

    if not database_exists(engine.url):
        create_database(engine.url)

    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def commit_session():
    try:
        driver_service.session.commit()
    except PendingRollbackError:
        driver_service.session.rollback()
        raise Exception
    except OperationalError:
        raise Exception


class Driver:

    def __init__(self):
        self.engine = get_engine()
        self.session = get_session(self.engine)


driver_service = Driver()
