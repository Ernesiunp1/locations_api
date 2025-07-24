import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()
DEV = os.getenv("DEV")

if DEV:
    # If in development mode, use the default SQLite database path
    SQLALCHEMY_DATABASE_URL = "sqlite:///./map.db"
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("DB_PATH", "sqlite:///./map.db")

# Db engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yields a database session for use in FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
