import sqlalchemy
from sqlalchemy.orm import declarative_base

from services.database.driver import get_engine

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    original_message_id = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    copy_message_id = sqlalchemy.Column(sqlalchemy.String(255))


Base.metadata.create_all(get_engine())
