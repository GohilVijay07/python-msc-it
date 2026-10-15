# ============================================================
# USER ROUTES (Protected - Profile)
# ============================================================

from fastapi import APIRouter, Depends

from models import UserDB
from auth import get_current_user


router = APIRouter()


# ---------- GET PROFILE (Protected) ----------

@router.get("/profile")
def get_profile(
    current_user: UserDB = Depends(get_current_user)
):

    return {
        "message": "Authentication successful!",
        "username": current_user.username,
        "full_name": current_user.full_name
    }
