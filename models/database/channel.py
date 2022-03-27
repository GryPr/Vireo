import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from services.database.driver import get_engine

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    channel_id = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    portal_id = sqlalchemy.Column(sqlalchemy.String(20))


Base.metadata.create_all(get_engine())
