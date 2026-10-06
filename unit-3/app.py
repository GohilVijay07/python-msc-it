from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


app = FastAPI()


# Database
engine = create_engine(
    "sqlite:///todo.db",
    connect_args={"check_same_thread": False}
)

Session = sessionmaker(bind=engine)

Base = declarative_base()


# Table
class Todo(Base):

    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


# Create table
Base.metadata.create_all(engine)


# Data format
class TodoData(BaseModel):

    title: str
    description: str


class UserData(BaseModel):

    username: str
    password: str


# =========================
# CREATE
# =========================

@app.post("/todo")
def add_todo(data: TodoData):

    db = Session()

    todo = Todo(
        title=data.title,
        description=data.description
    )

    db.add(todo)
    db.commit()

    db.close()

    return {"message": "Todo added"}


# =========================
# READ
# =========================

@app.get("/todo")
def get_todo():

    db = Session()

    todos = db.query(Todo).all()

    db.close()

    return todos


# =========================
# UPDATE
# =========================

@app.put("/todo/{id}")
def update_todo(id: int, data: TodoData):

    db = Session()

    todo = db.query(Todo).filter(Todo.id == id).first()

    if todo:
        todo.title = data.title
        todo.description = data.description

        db.commit()

        db.close()

        return {"message": "Todo updated"}

    db.close()

    return {"message": "Todo not found"}


# =========================
# DELETE
# =========================

@app.delete("/todo/{id}")
def delete_todo(id: int):

    db = Session()

    todo = db.query(Todo).filter(Todo.id == id).first()

    if todo:
        db.delete(todo)
        db.commit()

        db.close()

        return {"message": "Todo deleted"}

    db.close()

    return {"message": "Todo not found"}


# =========================
# USER / AUTH
# =========================

# 1. Register (Signup)
@app.post("/register")
def register(data: UserData):

    db = Session()

    # Check if username already exists
    existing_user = db.query(User).filter(User.username == data.username).first()
    if existing_user:
        db.close()
        return {"message": "Username already exists"}

    user = User(
        username=data.username,
        password=data.password
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "User registered successfully"}


# 2. Login
@app.post("/login")
def login(data: UserData):

    db = Session()

    user = db.query(User).filter(
        User.username == data.username,
        User.password == data.password
    ).first()

    db.close()

    if user:
        return {"message": "Login successful", "username": user.username}

    return {"message": "Invalid username or password"}


# 3. View All Users
@app.get("/users")
def get_users():

    db = Session()

    users = db.query(User).all()

    user_list = [{"id": u.id, "username": u.username, "password": u.password} for u in users]

    db.close()

    return user_list