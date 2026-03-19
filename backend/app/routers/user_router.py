from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_current_user
from app.models import Meme, User
from app.schemas import UserProfileResponse
from app.services import build_meme_card, serialize_user


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memes = db.scalars(
        select(Meme)
        .where(Meme.uploader_uid == current_user.uid)
        .options(selectinload(Meme.uploader))
        .order_by(Meme.pid.desc())
    ).all()
    items = [build_meme_card(db, meme, current_user) for meme in memes]
    return UserProfileResponse(user=serialize_user(current_user), submitted_memes=items)
