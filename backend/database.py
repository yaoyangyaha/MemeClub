# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ============================
# MySQL 数据库连接
# ============================

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/meme_site"

# ============================
# 创建引擎
# ============================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# ============================
# Session
# ============================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================
# Base 类
# ============================

Base = declarative_base()


# ============================
# 数据库初始化
# ============================

def init_db():
    import models
    Base.metadata.create_all(bind=engine)