# ============================================================
# PAGE ROUTES (Serve HTML Templates)
# ============================================================

import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ---------- Home → Redirect to Login ----------

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


# ---------- Login Page ----------

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


# ---------- Signup Page ----------

@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")


# ---------- Dashboard Page ----------

@router.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")
