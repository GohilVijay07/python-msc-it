# ============================================================
# DATABASE SETUP (SQLite / SQLAlchemy)
# ============================================================

import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env variables (searches current and parent directories)
load_dotenv(find_dotenv())

# Database URL from .env (defaults to sqlite:///todos.db)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///todos.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Session factory
Session = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()


# Dependency: get db session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
