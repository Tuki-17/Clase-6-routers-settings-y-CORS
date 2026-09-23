from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from app.core.config import settings

# connect_args fuerza los mensajes de error de PostgreSQL en inglés
# evitando el UnicodeDecodeError de psycopg2 en Windows con locale español
_connect_args: dict = {}
if "postgresql" in settings.DATABASE_URL:
    _connect_args = {"options": "-c lc_messages=en_US.UTF-8"}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()