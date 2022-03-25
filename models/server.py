import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Server(Base):
    __tablename__ = 'servers'
    server_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    portal_count = sqlalchemy.Column(sqlalchemy.Integer)