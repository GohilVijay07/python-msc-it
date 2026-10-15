# ============================================================
# DATABASE MODELS (SQLAlchemy)
# ============================================================

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base


# Todo Table - each todo belongs to a user
class Todo(Base):

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, default="")
    owner = Column(String, nullable=False)  # username of the todo owner
    completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # low, medium, high
    due_date = Column(String, nullable=True)     # e.g., "2026-10-08T18:00"
    created_at = Column(DateTime, default=datetime.now)


# User Table
class UserDB(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String)
