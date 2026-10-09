# ============================================================
# PYDANTIC SCHEMAS (Request / Response)
# ============================================================

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------- User Schemas ----------

class UserSignup(BaseModel):
    username: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    full_name: str


# ---------- Todo Schemas ----------

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None


class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    owner: str
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
