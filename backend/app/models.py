from datetime import datetime

from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    uid: Mapped[int] = mapped_column(primary_key=True, index=True)
    username_b64: Mapped[str] = mapped_column(
        VARCHAR(255, charset="ascii", collation="ascii_bin"),
        unique=True,
        nullable=False,
    )
    email_b64: Mapped[str] = mapped_column(
        VARCHAR(255, charset="ascii", collation="ascii_bin"),
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    user_status: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    memes: Mapped[list["Meme"]] = relationship(back_populates="uploader")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="user")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")


class Meme(Base):
    __tablename__ = "memes"

    pid: Mapped[int] = mapped_column(primary_key=True, index=True)
    title_b64: Mapped[str] = mapped_column(String(255), nullable=False)
    description_b64: Mapped[str] = mapped_column(Text, nullable=False)
    image_b64: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    review_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    uploader_uid: Mapped[int] = mapped_column(ForeignKey("users.uid"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    uploader: Mapped["User"] = relationship(back_populates="memes")
    comments: Mapped[list["Comment"]] = relationship(back_populates="meme")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="meme")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="meme")


class Comment(Base):
    __tablename__ = "comments"

    cid: Mapped[int] = mapped_column(primary_key=True, index=True)
    content_b64: Mapped[str] = mapped_column(String(512), nullable=False)
    meme_pid: Mapped[int] = mapped_column(ForeignKey("memes.pid"), nullable=False, index=True)
    user_uid: Mapped[int] = mapped_column(ForeignKey("users.uid"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    meme: Mapped["Meme"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("meme_pid", "user_uid", name="uq_ratings_meme_user"),)

    rid: Mapped[int] = mapped_column(primary_key=True, index=True)
    score: Mapped[float] = mapped_column(Numeric(2, 1), nullable=False)
    meme_pid: Mapped[int] = mapped_column(ForeignKey("memes.pid"), nullable=False, index=True)
    user_uid: Mapped[int] = mapped_column(ForeignKey("users.uid"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    meme: Mapped["Meme"] = relationship(back_populates="ratings")
    user: Mapped["User"] = relationship(back_populates="ratings")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("meme_pid", "user_uid", name="uq_favorites_meme_user"),)

    fid: Mapped[int] = mapped_column(primary_key=True, index=True)
    meme_pid: Mapped[int] = mapped_column(ForeignKey("memes.pid"), nullable=False, index=True)
    user_uid: Mapped[int] = mapped_column(ForeignKey("users.uid"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    meme: Mapped["Meme"] = relationship(back_populates="favorites")
    user: Mapped["User"] = relationship(back_populates="favorites")
