import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambiá postgres:postgres por tu usuario:contraseña de PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecommerce_db")

try:
    # Intentar conectar con PostgreSQL con un timeout de conexión corto
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"connect_timeout": 3} if "postgresql" in SQLALCHEMY_DATABASE_URL else {}
    )
    # Forzar una conexión rápida para verificar credenciales y existencia de DB
    with engine.connect() as conn:
        pass
    print("Conexión exitosa a la base de datos principal (PostgreSQL).")
except Exception as e:
    print(f"Error al conectar con PostgreSQL ({e}). Usando base de datos SQLite de respaldo...")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()