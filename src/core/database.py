from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models.models import Base

engine = create_engine("sqlite+pysqlite:///test.sqlite3", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    """Función de dependencia para obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
