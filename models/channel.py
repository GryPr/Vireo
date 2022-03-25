import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    channel_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    portal_id = sqlalchemy.Column(sqlalchemy.String)