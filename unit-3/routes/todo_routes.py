# ============================================================
# TODO ROUTES (Protected - Login Required)
# ============================================================

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session as DBSession

from database import get_db
from models import Todo, UserDB
from schemas import TodoCreate, TodoUpdate, TodoOut
from auth import get_current_user


router = APIRouter()


# ---------- CREATE TODO (Protected) ----------

@router.post("/todo")
def add_todo(
    data: TodoCreate,
    current_user: UserDB = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    todo = Todo(
        title=title,
        description=data.description or "",
        owner=current_user.username,
        priority=data.priority or "medium",
        due_date=data.due_date
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return {"message": "Todo added successfully", "id": todo.id}


# ---------- READ ALL TODOS (Protected - only your todos) ----------

@router.get("/todo")
def get_todos(
    current_user: UserDB = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    todos = db.query(Todo).filter(
        Todo.owner == current_user.username
    ).order_by(Todo.id.desc()).all()

    return todos


# ---------- TOGGLE TODO STATUS (Protected) ----------

@router.patch("/todo/{id}/toggle")
def toggle_todo(
    id: int,
    current_user: UserDB = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.owner == current_user.username
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.completed = not bool(todo.completed)
    db.commit()

    return {"message": "Status updated", "completed": todo.completed}


# ---------- UPDATE TODO (Protected) ----------

@router.put("/todo/{id}")
def update_todo(
    id: int,
    data: TodoUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.owner == current_user.username
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    if data.title is not None:
        title = data.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        todo.title = title

    if data.description is not None:
        todo.description = data.description

    if data.completed is not None:
        todo.completed = data.completed

    if data.priority is not None:
        todo.priority = data.priority

    if data.due_date is not None:
        todo.due_date = data.due_date

    db.commit()

    return {"message": "Todo updated successfully"}


# ---------- DELETE TODO (Protected) ----------

@router.delete("/todo/{id}")
def delete_todo(
    id: int,
    current_user: UserDB = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == id,
        Todo.owner == current_user.username
    ).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
