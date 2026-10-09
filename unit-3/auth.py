# ============================================================
# JWT AUTHENTICATION
# ============================================================

import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session as DBSession
import jwt

from database import get_db
from models import UserDB

# Load .env variables (searches current and parent directories)
load_dotenv(find_dotenv())

# JWT Config from environment variables with fallback defaults
SECRET_KEY = os.getenv("SECRET_KEY", "VtSzMe3tQ3PbCb4ZSC0dUXP2LgRD3C78XbR8uBs4q9Q=")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------- Create JWT Token ----------

def create_token(username: str, full_name: str) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "name": full_name,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ---------- Get Current User from JWT ----------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: DBSession = Depends(get_db)
):

    try:

        # Decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        # Find user in database
        user = db.query(UserDB).filter(
            UserDB.username == username
        ).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
