import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

import models
from database import SessionLocal

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 365
PAGE_SIZE = 50

app = FastAPI(title="MemeClub API")

DEFAULT_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]

raw_origins = os.getenv("CORS_ALLOW_ORIGINS", "")
cors_allow_origins = [item.strip() for item in raw_origins.split(",") if item.strip()] or DEFAULT_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterBody(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=255)
    email: EmailStr


class LoginBody(BaseModel):
    username: str
    password: str


class UploadBody(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=4000)
    image_base64: str = Field(min_length=10)


class RateBody(BaseModel):
    pid: int
    rating: float = Field(ge=0.5, le=5.0)


class CommentBody(BaseModel):
    pid: int
    content: str = Field(min_length=1, max_length=100)


class FavoriteBody(BaseModel):
    pid: int


class BanBody(BaseModel):
    uid: int
    banned: bool


class ReviewBody(BaseModel):
    status: str = Field(pattern="^(approved|rejected)$")


class AdminBanUploaderBody(BaseModel):
    uid: int


# ------------------------------
# DB
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# Auth helpers
# ------------------------------
def create_token(uid: int):
    payload = {
        "uid": uid,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["uid"])
    except Exception as exc:
        raise HTTPException(status_code=401, detail="token invalid") from exc


def get_current_user(
    db: Session = Depends(get_db),
    token_cookie: Optional[str] = Cookie(default=None, alias="token"),
    authorization: Optional[str] = Header(default=None),
):
    token = token_cookie
    if not token and authorization:
        scheme, _, credentials = authorization.partition(" ")
        if scheme.lower() == "bearer" and credentials:
            token = credentials

    if not token:
        raise HTTPException(status_code=401, detail="login required")

    uid = decode_token(token)
    user = db.query(models.User).filter_by(uid=uid).first()
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    return user


def get_optional_user(
    db: Session = Depends(get_db),
    token_cookie: Optional[str] = Cookie(default=None, alias="token"),
    authorization: Optional[str] = Header(default=None),
):
    token = token_cookie
    if not token and authorization:
        scheme, _, credentials = authorization.partition(" ")
        if scheme.lower() == "bearer" and credentials:
            token = credentials

    if not token:
        return None

    try:
        uid = decode_token(token)
    except HTTPException:
        return None

    return db.query(models.User).filter_by(uid=uid).first()


def get_admin_user(user: models.User = Depends(get_current_user)):
    if user.user_status != "admin":
        raise HTTPException(status_code=403, detail="admin only")
    return user


def meme_to_dict(meme: models.Meme, uid: Optional[int], db: Session):
    avg_rating = db.query(func.avg(models.Rating.rating)).filter_by(pid=meme.pid).scalar() or 0
    favorite = False
    user_rating = None
    if uid is not None:
        favorite = db.query(models.Favorite).filter_by(uid=uid, pid=meme.pid).first() is not None
        existing_rating = db.query(models.Rating).filter_by(uid=uid, pid=meme.pid).first()
        user_rating = existing_rating.rating if existing_rating else None

    return {
        "pid": meme.pid,
        "title": meme.title,
        "description": meme.description,
        "image_base64": meme.image_base64,
        "uploader_uid": meme.uploader_uid,
        "uploader_name": meme.uploader.username if meme.uploader else "",
        "status": meme.status,
        "created_at": meme.created_at.isoformat() if meme.created_at else None,
        "avg_rating": round(float(avg_rating), 2),
        "is_favorite": favorite,
        "user_rating": user_rating,
    }


@app.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
    exist = db.query(models.User).filter_by(username=body.username).first()
    if exist:
        raise HTTPException(400, "username exists")

    user = models.User(
        username=body.username,
        password=body.password,
        email=body.email,
        user_status="user",
        is_banned=False,
        created_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    return {"msg": "register success"}


@app.post("/login")
def login(body: LoginBody, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=body.username, password=body.password).first()
    if not user:
        raise HTTPException(401, "login failed")

    token = create_token(user.uid)
    response.set_cookie(
        key="token",
        value=token,
        max_age=TOKEN_EXPIRE_DAYS * 24 * 3600,
        httponly=True,
        samesite="lax",
    )
    return {"token": token, "uid": user.uid, "username": user.username, "user_status": user.user_status}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return {"msg": "logout success"}


@app.get("/me")
def me(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    my_memes = (
        db.query(models.Meme)
        .filter_by(uploader_uid=user.uid)
        .order_by(models.Meme.pid.desc())
        .all()
    )
    return {
        "uid": user.uid,
        "username": user.username,
        "email": user.email,
        "is_banned": user.is_banned,
        "user_status": user.user_status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "my_memes": [meme_to_dict(item, user.uid, db) for item in my_memes],
    }


@app.post("/upload")
def upload(body: UploadBody, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_banned:
        raise HTTPException(status_code=403, detail="user banned")

    meme = models.Meme(
        title=body.title,
        description=body.description,
        image_base64=body.image_base64,
        uploader_uid=user.uid,
        status="pending",
        created_at=datetime.utcnow(),
    )
    db.add(meme)
    db.commit()
    return {"msg": "upload success"}


@app.get("/memes")
def get_memes(page: int = 1, q: str = "", user: Optional[models.User] = Depends(get_optional_user), db: Session = Depends(get_db)):
    query = db.query(models.Meme).filter(models.Meme.status == "approved")
    if q:
        query = query.filter(or_(models.Meme.title.like(f"%{q}%"), models.Meme.description.like(f"%{q}%")))

    total = query.count()
    memes = query.order_by(models.Meme.pid.desc()).offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()

    return {
        "items": [meme_to_dict(item, user.uid if user else None, db) for item in memes],
        "page": page,
        "page_size": PAGE_SIZE,
        "total": total,
    }


@app.get("/meme/{pid}")
def get_meme_detail(pid: int, user: Optional[models.User] = Depends(get_optional_user), db: Session = Depends(get_db)):
    meme = db.query(models.Meme).filter_by(pid=pid, status="approved").first()
    if not meme:
        raise HTTPException(404, "meme not found")

    comments = (
        db.query(models.Comment)
        .filter_by(pid=pid)
        .order_by(models.Comment.id.desc())
        .all()
    )
    return {
        **meme_to_dict(meme, user.uid if user else None, db),
        "comments": [
            {
                "id": c.id,
                "uid": c.uid,
                "username": c.user.username if c.user else "",
                "content": c.content,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in comments
        ],
        "comment_count": len(comments),
    }


@app.post("/rate")
def rate(body: RateBody, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    old = db.query(models.Rating).filter_by(uid=user.uid, pid=body.pid).first()
    if old:
        old.rating = body.rating
    else:
        db.add(models.Rating(uid=user.uid, pid=body.pid, rating=body.rating))
    db.commit()
    return {"msg": "rated"}


@app.post("/comment")
def comment(body: CommentBody, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.is_banned:
        raise HTTPException(403, "banned")

    c = models.Comment(uid=user.uid, pid=body.pid, content=body.content, created_at=datetime.utcnow())
    db.add(c)
    db.commit()
    return {"msg": "comment success"}


@app.post("/favorite")
def favorite(body: FavoriteBody, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    fav = db.query(models.Favorite).filter_by(uid=user.uid, pid=body.pid).first()
    if fav:
        db.delete(fav)
        db.commit()
        return {"msg": "unfavorite", "is_favorite": False}

    db.add(models.Favorite(uid=user.uid, pid=body.pid))
    db.commit()
    return {"msg": "favorite", "is_favorite": True}


@app.get("/admin/pending")
def pending_memes(admin: models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    memes = db.query(models.Meme).filter_by(status="pending").order_by(models.Meme.pid.desc()).all()
    return {"items": [meme_to_dict(item, admin.uid, db) for item in memes]}


@app.post("/admin/meme/{pid}/review")
def review_meme(pid: int, body: ReviewBody, admin: models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    meme = db.query(models.Meme).filter_by(pid=pid).first()
    if not meme:
        raise HTTPException(404, "meme not found")
    meme.status = body.status
    db.commit()
    return {"msg": "reviewed"}


@app.post("/admin/ban")
def admin_ban_user(body: BanBody, admin: models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if body.uid == admin.uid:
        raise HTTPException(400, "cannot ban self")
    target = db.query(models.User).filter_by(uid=body.uid).first()
    if not target:
        raise HTTPException(404, "user not found")
    target.is_banned = body.banned
    db.commit()
    return {"msg": "updated", "uid": target.uid, "is_banned": target.is_banned}


@app.post("/admin/ban-uploader")
def admin_ban_uploader(body: AdminBanUploaderBody, admin: models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target = db.query(models.User).filter_by(uid=body.uid).first()
    if not target:
        raise HTTPException(404, "user not found")
    if target.uid == admin.uid:
        raise HTTPException(status_code=400, detail="cannot ban self")
    target.is_banned = True
    db.commit()
    return {"msg": "uploader banned"}


@app.get("/admin/users")
def list_users(admin: models.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.uid.asc()).all()
    return {
        "items": [
            {
                "uid": u.uid,
                "username": u.username,
                "email": u.email,
                "user_status": u.user_status,
                "is_banned": u.is_banned,
            }
            for u in users
        ]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
