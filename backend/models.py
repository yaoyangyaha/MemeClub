from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from database import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(100))
    user_status = Column(String(20))
    is_banned = Column(Boolean)


class Meme(Base):
    __tablename__ = "memes"

    pid = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    image_base64 = Column(Text)
    uploader_uid = Column(Integer)
    status = Column(String(20))
