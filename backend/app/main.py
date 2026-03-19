from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import admin_router, auth_router, meme_router, user_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="MemeClub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router.router)
app.include_router(meme_router.router)
app.include_router(user_router.router)
app.include_router(admin_router.router)
