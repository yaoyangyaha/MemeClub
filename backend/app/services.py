from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.codec import decode_text, encode_text
from app.models import Comment, Favorite, Meme, Rating, User
from app.schemas import CommentItem, MemeCardItem, MemeDetailResponse, UserSummary


def serialize_user(user: User) -> UserSummary:
    return UserSummary(
        uid=user.uid,
        username=decode_text(user.username_b64),
        email=decode_text(user.email_b64),
        user_status=user.user_status,
        is_banned=user.is_banned,
        created_at=user.created_at,
    )


def find_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username_b64 == encode_text(username)))


def find_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email_b64 == encode_text(email.lower())))


def build_meme_card(db: Session, meme: Meme, viewer: User | None) -> MemeCardItem:
    avg_rating = db.scalar(select(func.avg(Rating.score)).where(Rating.meme_pid == meme.pid)) or 0
    favorite_count = db.scalar(select(func.count(Favorite.fid)).where(Favorite.meme_pid == meme.pid)) or 0
    comment_count = db.scalar(select(func.count(Comment.cid)).where(Comment.meme_pid == meme.pid)) or 0
    is_favorited = False
    if viewer:
        is_favorited = (
            db.scalar(
                select(func.count(Favorite.fid)).where(
                    Favorite.meme_pid == meme.pid,
                    Favorite.user_uid == viewer.uid,
                )
            )
            or 0
        ) > 0

    return MemeCardItem(
        pid=meme.pid,
        title=decode_text(meme.title_b64),
        image_base64=meme.image_b64,
        created_at=meme.created_at,
        uploader_uid=meme.uploader.uid,
        uploader_name=decode_text(meme.uploader.username_b64),
        uploader_email=decode_text(meme.uploader.email_b64),
        review_status=meme.review_status,
        average_rating=float(avg_rating),
        favorite_count=favorite_count,
        comment_count=comment_count,
        is_favorited=is_favorited,
    )


def build_meme_detail(db: Session, meme: Meme, viewer: User | None) -> MemeDetailResponse:
    avg_rating = db.scalar(select(func.avg(Rating.score)).where(Rating.meme_pid == meme.pid)) or 0
    favorite_count = db.scalar(select(func.count(Favorite.fid)).where(Favorite.meme_pid == meme.pid)) or 0
    comments = db.scalars(
        select(Comment)
        .where(Comment.meme_pid == meme.pid)
        .options(selectinload(Comment.user))
        .order_by(Comment.cid.desc())
    ).all()
    comment_items = [
        CommentItem(
            cid=comment.cid,
            content=decode_text(comment.content_b64),
            created_at=comment.created_at,
            user_uid=comment.user.uid,
            username=decode_text(comment.user.username_b64),
            email=decode_text(comment.user.email_b64),
        )
        for comment in comments
    ]

    user_rating = None
    is_favorited = False
    if viewer:
        rating = db.scalar(
            select(Rating).where(Rating.meme_pid == meme.pid, Rating.user_uid == viewer.uid)
        )
        if rating:
            user_rating = float(rating.score)
        is_favorited = (
            db.scalar(
                select(func.count(Favorite.fid)).where(
                    Favorite.meme_pid == meme.pid,
                    Favorite.user_uid == viewer.uid,
                )
            )
            or 0
        ) > 0

    return MemeDetailResponse(
        pid=meme.pid,
        title=decode_text(meme.title_b64),
        description=decode_text(meme.description_b64),
        image_base64=meme.image_b64,
        created_at=meme.created_at,
        review_status=meme.review_status,
        uploader_uid=meme.uploader.uid,
        uploader_name=decode_text(meme.uploader.username_b64),
        uploader_email=decode_text(meme.uploader.email_b64),
        average_rating=float(avg_rating),
        user_rating=user_rating,
        favorite_count=favorite_count,
        comment_count=len(comment_items),
        is_favorited=is_favorited,
        comments=comment_items,
    )
