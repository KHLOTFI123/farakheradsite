from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, verify_password
from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import LoginIn, TokenOut
from app.security import rate_limit

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    rate_limit(
        request,
        name="login",
        limit=settings.login_rate_limit,
        window_seconds=300,
    )
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="نام کاربری یا رمز عبور نادرست است",
        )
    return TokenOut(access_token=create_access_token(user.username))
