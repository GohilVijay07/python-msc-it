# ============================================================
# MAIN APP - FastAPI Entry Point
# ============================================================

import os
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from database import engine
from models import Base

# Load .env variables
load_dotenv(find_dotenv())

# Import route files
from routes import auth_routes, todo_routes, user_routes, page_routes


# Drop old 'todo' table (from previous code) if it exists
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS todo"))
    conn.commit()

# Create all tables
Base.metadata.create_all(engine)

# Auto-migrate SQLite schema for todos table
with engine.connect() as conn:
    res = conn.execute(text("PRAGMA table_info(todos);")).fetchall()
    existing_cols = [r[1] for r in res]
    if "completed" not in existing_cols:
        conn.execute(text("ALTER TABLE todos ADD COLUMN completed BOOLEAN DEFAULT 0"))
    if "priority" not in existing_cols:
        conn.execute(text("ALTER TABLE todos ADD COLUMN priority VARCHAR DEFAULT 'medium'"))
    if "due_date" not in existing_cols:
        conn.execute(text("ALTER TABLE todos ADD COLUMN due_date VARCHAR DEFAULT NULL"))
    if "created_at" not in existing_cols:
        conn.execute(text("ALTER TABLE todos ADD COLUMN created_at DATETIME DEFAULT NULL"))
        conn.execute(text("UPDATE todos SET created_at = datetime('now') WHERE created_at IS NULL"))
    conn.commit()


# Create FastAPI app
app_title = os.getenv("APP_NAME", "Todo App with JWT Authentication")
app = FastAPI(title=app_title)


# Base directory for resolving static and template assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files (CSS, JS)
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Register API routes
app.include_router(auth_routes.router)
app.include_router(todo_routes.router)
app.include_router(user_routes.router)

# Register Page routes (HTML templates)
app.include_router(page_routes.router)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    uvicorn.run("app:app", host=host, port=port, reload=reload)