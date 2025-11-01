from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from models.models import Base

engine = create_engine("sqlite+pysqlite:///test.sqlite3", echo=True)


def create_tables():
    Base.metadata.create_all(engine)


def get_session():
    return sessionmaker(bind=engine)
