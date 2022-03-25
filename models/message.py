import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    original_message_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    copy_message_id = sqlalchemy.Column(sqlalchemy.String)