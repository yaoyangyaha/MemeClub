from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import require_admin
from app.models import Meme, User
from app.schemas import BanUserRequest, ReviewMemeRequest
from app.services import build_meme_card


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/ban-user")
def ban_user(
    payload: BanUserRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = db.get(User, payload.uid)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    if user.user_status == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能封禁管理员")
    user.is_banned = payload.banned
    db.commit()
    return {"message": "用户状态已更新"}


@router.get("/pending-memes")
def list_pending_memes(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    memes = db.scalars(
        select(Meme)
        .where(Meme.review_status == "pending")
        .options(selectinload(Meme.uploader))
        .order_by(Meme.pid.desc())
    ).all()
    return [build_meme_card(db, meme, admin) for meme in memes]


@router.post("/memes/{pid}/review")
def review_meme(
    pid: int,
    payload: ReviewMemeRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    meme = db.scalar(
        select(Meme).where(Meme.pid == pid).options(selectinload(Meme.uploader))
    )
    if not meme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="梗图不存在")
    meme.review_status = "approved" if payload.action == "approve" else "rejected"
    if payload.ban_uploader and meme.uploader.user_status != "admin":
        meme.uploader.is_banned = True
    db.commit()
    return {"message": "审核结果已保存"}
