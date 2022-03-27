import sqlalchemy
from sqlalchemy.orm import declarative_base

from services.database.driver import get_engine

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    original_message_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    copy_message_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    channel_id = sqlalchemy.Column(sqlalchemy.BigInteger)


Base.metadata.create_all(get_engine())
