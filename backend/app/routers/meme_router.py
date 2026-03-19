from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.codec import decode_text, encode_text
from app.database import get_db
from app.deps import ensure_not_banned, get_current_user, get_optional_user
from app.models import Comment, Favorite, Meme, Rating, User
from app.schemas import (
    CommentCreateRequest,
    FavoriteResponse,
    MemeCreateRequest,
    MemeListResponse,
    RatingCreateRequest,
)
from app.services import build_meme_card, build_meme_detail


router = APIRouter(prefix="/api/memes", tags=["memes"])


@router.get("", response_model=MemeListResponse)
def list_memes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=50),
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
    viewer: User | None = Depends(get_optional_user),
):
    memes = db.scalars(
        select(Meme)
        .where(Meme.review_status == "approved")
        .options(selectinload(Meme.uploader))
        .order_by(Meme.pid.desc())
    ).all()

    if keyword.strip():
        lowered = keyword.strip().lower()
        memes = [
            meme
            for meme in memes
            if lowered in decode_text(meme.title_b64).lower()
            or lowered in decode_text(meme.description_b64).lower()
            or lowered in decode_text(meme.uploader.username_b64).lower()
        ]

    total = len(memes)
    start = (page - 1) * page_size
    end = start + page_size
    items = [build_meme_card(db, meme, viewer) for meme in memes[start:end]]
    return MemeListResponse(total=total, page=page, page_size=page_size, items=items)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_meme(
    payload: MemeCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_not_banned(current_user)
    meme = Meme(
        title_b64=encode_text(payload.title),
        description_b64=encode_text(payload.description),
        image_b64=payload.image_base64,
        uploader_uid=current_user.uid,
        review_status="pending",
    )
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return {"message": "梗图已提交，等待管理员审核", "pid": meme.pid}


@router.get("/{pid}")
def get_meme_detail(
    pid: int,
    db: Session = Depends(get_db),
    viewer: User | None = Depends(get_optional_user),
):
    meme = db.scalar(
        select(Meme).where(Meme.pid == pid).options(selectinload(Meme.uploader))
    )
    if not meme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="梗图不存在")
    can_view = meme.review_status == "approved"
    if viewer and (viewer.user_status == "admin" or viewer.uid == meme.uploader_uid):
        can_view = True
    if not can_view:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="该梗图暂不可查看")

    return build_meme_detail(db, meme, viewer)


@router.post("/{pid}/ratings")
def rate_meme(
    pid: int,
    payload: RatingCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meme = db.get(Meme, pid)
    if not meme or meme.review_status != "approved":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="梗图不存在")
    if payload.score * 2 != int(payload.score * 2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="评分仅支持半星")

    rating = db.scalar(select(Rating).where(Rating.meme_pid == pid, Rating.user_uid == current_user.uid))
    if rating:
        rating.score = payload.score
    else:
        db.add(Rating(score=payload.score, meme_pid=pid, user_uid=current_user.uid))
    db.commit()
    return {"message": "评分已提交"}


@router.post("/{pid}/favorite", response_model=FavoriteResponse)
def toggle_favorite(
    pid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meme = db.get(Meme, pid)
    if not meme or meme.review_status != "approved":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="梗图不存在")

    favorite = db.scalar(
        select(Favorite).where(Favorite.meme_pid == pid, Favorite.user_uid == current_user.uid)
    )
    if favorite:
        db.delete(favorite)
        db.commit()
        return FavoriteResponse(favorited=False)

    db.add(Favorite(meme_pid=pid, user_uid=current_user.uid))
    db.commit()
    return FavoriteResponse(favorited=True)


@router.post("/{pid}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
    pid: int,
    payload: CommentCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ensure_not_banned(current_user)
    meme = db.get(Meme, pid)
    if not meme or meme.review_status != "approved":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="梗图不存在")

    comment = Comment(
        content_b64=encode_text(payload.content),
        meme_pid=pid,
        user_uid=current_user.uid,
    )
    db.add(comment)
    db.commit()
    return {"message": "评论已提交"}
