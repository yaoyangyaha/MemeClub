# models.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# ============================
# 用户表
# ============================

class User(Base):

    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    email = Column(String(100), nullable=False)

    user_status = Column(String(20), default="user")

    is_banned = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    memes = relationship("Meme", back_populates="uploader")

    comments = relationship("Comment", back_populates="user")

    ratings = relationship("Rating", back_populates="user")

    favorites = relationship("Favorite", back_populates="user")


# ============================
# 梗图表
# ============================

class Meme(Base):

    __tablename__ = "memes"

    pid = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    description = Column(Text)

    image_base64 = Column(Text, nullable=False)

    uploader_uid = Column(Integer, ForeignKey("users.uid"))

    status = Column(String(20), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    uploader = relationship("User", back_populates="memes")

    comments = relationship("Comment", back_populates="meme")

    ratings = relationship("Rating", back_populates="meme")

    favorites = relationship("Favorite", back_populates="meme")


# ============================
# 评分表
# ============================

class Rating(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)

    uid = Column(Integer, ForeignKey("users.uid"))

    pid = Column(Integer, ForeignKey("memes.pid"))

    rating = Column(Float)

    # 关系
    user = relationship("User", back_populates="ratings")

    meme = relationship("Meme", back_populates="ratings")


# ============================
# 评论表
# ============================

class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    uid = Column(Integer, ForeignKey("users.uid"))

    pid = Column(Integer, ForeignKey("memes.pid"))

    content = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="comments")

    meme = relationship("Meme", back_populates="comments")


# ============================
# 收藏表
# ============================

class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)

    uid = Column(Integer, ForeignKey("users.uid"))

    pid = Column(Integer, ForeignKey("memes.pid"))

    # 关系
    user = relationship("User", back_populates="favorites")

    meme = relationship("Meme", back_populates="favorites")