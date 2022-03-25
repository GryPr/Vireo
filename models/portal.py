import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Portal(Base):
    __tablename__ = 'portals'
    portal_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    primary_channel_id = sqlalchemy.Column(sqlalchemy.String)