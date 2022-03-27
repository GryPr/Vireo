import sqlalchemy
from sqlalchemy.orm import declarative_base

from services.database.driver import get_engine

Base = declarative_base()


class PortalRoles(Base):
    __tablename__ = 'portal_roles'
    role_id = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    portal_id = sqlalchemy.Column(sqlalchemy.String(20))
    role_name = sqlalchemy.Column(sqlalchemy.String(255))


Base.metadata.create_all(get_engine())
