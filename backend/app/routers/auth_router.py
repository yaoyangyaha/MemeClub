from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.codec import encode_text
from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import AuthResponse, LoginRequest, RegisterRequest
from app.services import find_user_by_email, find_user_by_username, serialize_user


router = APIRouter(prefix="/api/auth", tags=["auth"])


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        max_age=settings.access_token_expire_seconds,
        expires=settings.access_token_expire_seconds,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
    )


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    if find_user_by_username(db, payload.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    if find_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已存在")

    user = User(
        username_b64=encode_text(payload.username),
        email_b64=encode_text(payload.email.lower()),
        password_hash=hash_password(payload.password),
        user_status="user",
        is_banned=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.uid)
    set_auth_cookie(response, token)
    return AuthResponse(access_token=token, user=serialize_user(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = find_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")

    token = create_access_token(user.uid)
    set_auth_cookie(response, token)
    return AuthResponse(access_token=token, user=serialize_user(user))


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=settings.cookie_name, httponly=True, secure=settings.cookie_secure, samesite="lax")
    return {"message": "已退出登录"}


@router.get("/me", response_model=AuthResponse)
def me(current_user: User = Depends(get_current_user)):
    token = create_access_token(current_user.uid)
    return AuthResponse(access_token=token, user=serialize_user(current_user))
