# ============================================================
# AUTH ROUTES (Signup + Login)
# ============================================================

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session as DBSession

from database import get_db
from models import UserDB
from schemas import UserSignup, UserLogin
from auth import create_token


router = APIRouter()


# ---------- SIGNUP ----------

@router.post("/signup")
def signup(
    user: UserSignup,
    db: DBSession = Depends(get_db)
):

    # Check if user already exists
    existing = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Create new user
    new_user = UserDB(
        username=user.username,
        password=user.password,
        full_name=user.full_name
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User created successfully",
        "username": user.username
    }


# ---------- LOGIN ----------

@router.post("/login")
def login(
    user: UserLogin,
    db: DBSession = Depends(get_db)
):

    # Find user
    db_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Check password
    if user.password != db_user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Generate JWT token
    token = create_token(db_user.username, db_user.full_name)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
