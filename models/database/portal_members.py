import sqlalchemy
from sqlalchemy.orm import declarative_base

from services.database.driver import get_engine

Base = declarative_base()


class PortalMembers(Base):
    __tablename__ = 'portals'
    portal_id = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.String(20))
    role_id = sqlalchemy.Column(sqlalchemy.String(20))


Base.metadata.create_all(get_engine())
