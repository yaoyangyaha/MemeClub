from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False)
    user_status = Column(String(20), default="user", nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    memes = relationship("Meme", back_populates="uploader")
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Meme(Base):
    __tablename__ = "memes"

    pid = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    image_base64 = Column(Text, nullable=False)
    uploader_uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("User", back_populates="memes")
    comments = relationship("Comment", back_populates="meme")
    ratings = relationship("Rating", back_populates="meme")
    favorites = relationship("Favorite", back_populates="meme")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("memes.pid"), nullable=False)
    rating = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint("uid", "pid", name="uq_rating_uid_pid"),)

    user = relationship("User", back_populates="ratings")
    meme = relationship("Meme", back_populates="ratings")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("memes.pid"), nullable=False)
    content = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    meme = relationship("Meme", back_populates="comments")


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"), nullable=False)
    pid = Column(Integer, ForeignKey("memes.pid"), nullable=False)

    __table_args__ = (UniqueConstraint("uid", "pid", name="uq_favorite_uid_pid"),)

    user = relationship("User", back_populates="favorites")
    meme = relationship("Meme", back_populates="favorites")
