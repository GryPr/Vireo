import sqlalchemy
from sqlalchemy.orm import declarative_base

from services.database.driver import get_engine

Base = declarative_base()


class Server(Base):
    __tablename__ = 'servers'
    server_id = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    portal_count = sqlalchemy.Column(sqlalchemy.String(20))


Base.metadata.create_all(get_engine())
