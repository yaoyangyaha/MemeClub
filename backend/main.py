from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime, timedelta
import jwt

import models
from database import SessionLocal

SECRET_KEY = "SUPER_SECRET_KEY"

app = FastAPI()


# ------------------------------
# 数据库依赖
# ------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ------------------------------
# JWT
# ------------------------------

def create_token(uid: int):
    payload = {
        "uid": uid,
        "exp": datetime.utcnow() + timedelta(days=365)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["uid"]
    except:
        raise HTTPException(401, "token invalid")


# ------------------------------
# 注册
# ------------------------------

@app.post("/register")
def register(
        username: str,
        password: str,
        email: str,
        db: Session = Depends(get_db)
):
    exist = db.query(models.User).filter_by(username=username).first()

    if exist:
        raise HTTPException(400, "username exists")

    user = models.User(
        username=username,
        password=password,
        email=email,
        user_status="user",
        is_banned=False,
        created_at=datetime.now()
    )

    db.add(user)
    db.commit()

    return {"msg": "register success"}


# ------------------------------
# 登录
# ------------------------------

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(
        username=username,
        password=password
    ).first()

    if not user:
        raise HTTPException(401, "login failed")

    token = create_token(user.uid)

    return {
        "token": token,
        "uid": user.uid,
        "username": user.username
    }


# ------------------------------
# 上传梗图
# ------------------------------

@app.post("/upload")
def upload(
        title: str,
        description: str,
        image_base64: str,
        uid: int,
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(uid=uid).first()

    if user.is_banned:
        raise HTTPException(403, "user banned")

    meme = models.Meme(
        title=title,
        description=description,
        image_base64=image_base64,
        uploader_uid=uid,
        status="pending",
        created_at=datetime.now()
    )

    db.add(meme)
    db.commit()

    return {"msg": "upload success"}


# ------------------------------
# 首页梗图分页
# ------------------------------

@app.get("/memes")
def get_memes(page: int = 1, db: Session = Depends(get_db)):
    size = 50

    memes = db.query(
        models.Meme,
        func.avg(models.Rating.rating).label("avg_rating")
    ).outerjoin(
        models.Rating,
        models.Meme.pid == models.Rating.pid
    ).filter(
        models.Meme.status == "approved"
    ).group_by(
        models.Meme.pid
    ).order_by(
        models.Meme.pid.desc()
    ).offset((page - 1) * size).limit(size).all()

    return memes


# ------------------------------
# 搜索
# ------------------------------

@app.get("/search")
def search(q: str, page: int = 1, db: Session = Depends(get_db)):
    size = 50

    memes = db.query(models.Meme).filter(
        models.Meme.status == "approved",
        or_(
            models.Meme.title.like(f"%{q}%"),
            models.Meme.description.like(f"%{q}%")
        )
    ).order_by(
        models.Meme.pid.desc()
    ).offset((page - 1) * size).limit(size).all()

    return memes


# ------------------------------
# 提交评分
# ------------------------------

@app.post("/rate")
def rate(uid: int, pid: int, rating: float, db: Session = Depends(get_db)):
    old = db.query(models.Rating).filter_by(uid=uid, pid=pid).first()

    if old:
        old.rating = rating
    else:
        db.add(models.Rating(uid=uid, pid=pid, rating=rating))

    db.commit()

    return {"msg": "rated"}


# ------------------------------
# 评论
# ------------------------------

@app.post("/comment")
def comment(uid: int, pid: int, content: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(uid=uid).first()

    if user.is_banned:
        raise HTTPException(403, "banned")

    c = models.Comment(
        uid=uid,
        pid=pid,
        content=content,
        created_at=datetime.now()
    )

    db.add(c)
    db.commit()

    return {"msg": "comment success"}


# ------------------------------
# 评论列表
# ------------------------------

@app.get("/comments")
def get_comments(pid: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter_by(pid=pid).all()

    return comments


# ------------------------------
# 收藏
# ------------------------------

@app.post("/favorite")
def favorite(uid: int, pid: int, db: Session = Depends(get_db)):
    fav = db.query(models.Favorite).filter_by(uid=uid, pid=pid).first()

    if fav:
        db.delete(fav)
        db.commit()
        return {"msg": "unfavorite"}

    else:
        f = models.Favorite(uid=uid, pid=pid)
        db.add(f)
        db.commit()

        return {"msg": "favorite"}


# ------------------------------
# 用户中心
# ------------------------------

@app.get("/user")
def user_info(uid: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(uid=uid).first()

    memes = db.query(models.Meme).filter_by(
        uploader_uid=uid
    ).all()

    return {
        "uid": user.uid,
        "username": user.username,
        "is_banned": user.is_banned,
        "memes": memes
    }


# ------------------------------
# 管理员审核图片
# ------------------------------

@app.get("/admin/pending")
def pending_memes(db: Session = Depends(get_db)):
    memes = db.query(models.Meme).filter_by(status="pending").all()

    return memes


@app.post("/admin/approve")
def approve(pid: int, db: Session = Depends(get_db)):
    meme = db.query(models.Meme).filter_by(pid=pid).first()

    meme.status = "approved"

    db.commit()

    return {"msg": "approved"}


@app.post("/admin/reject")
def reject(pid: int, db: Session = Depends(get_db)):
    meme = db.query(models.Meme).filter_by(pid=pid).first()

    meme.status = "rejected"

    db.commit()

    return {"msg": "rejected"}


# ------------------------------
# 管理员封禁用户
# ------------------------------

@app.post("/admin/ban")
def ban_user(uid: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(uid=uid).first()

    user.is_banned = True

    db.commit()

    return {"msg": "user banned"}


@app.post("/admin/unban")
def unban(uid: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(uid=uid).first()

    user.is_banned = False

    db.commit()

    return {"msg": "user unbanned"}
