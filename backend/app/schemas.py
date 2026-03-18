from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)


class LoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=6, max_length=64)


class UserSummary(BaseModel):
    uid: int
    username: str
    email: str
    user_status: str
    is_banned: bool
    created_at: datetime


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSummary


class MemeCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=60)
    description: str = Field(min_length=1, max_length=2000)
    image_base64: str = Field(min_length=50)


class CommentCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=100)


class RatingCreateRequest(BaseModel):
    score: float = Field(ge=0.5, le=5.0)


class FavoriteResponse(BaseModel):
    favorited: bool


class CommentItem(BaseModel):
    cid: int
    content: str
    created_at: datetime
    user_uid: int
    username: str
    email: str


class MemeCardItem(BaseModel):
    pid: int
    title: str
    image_base64: str
    created_at: datetime
    uploader_uid: int
    uploader_name: str
    uploader_email: str
    review_status: str
    average_rating: float
    favorite_count: int
    comment_count: int
    is_favorited: bool


class MemeListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[MemeCardItem]


class MemeDetailResponse(BaseModel):
    pid: int
    title: str
    description: str
    image_base64: str
    created_at: datetime
    review_status: str
    uploader_uid: int
    uploader_name: str
    uploader_email: str
    average_rating: float
    user_rating: float | None
    favorite_count: int
    comment_count: int
    is_favorited: bool
    comments: list[CommentItem]


class UserProfileResponse(BaseModel):
    user: UserSummary
    submitted_memes: list[MemeCardItem]


class BanUserRequest(BaseModel):
    uid: int
    banned: bool


class ReviewMemeRequest(BaseModel):
    action: Literal["approve", "reject"]
    ban_uploader: bool = False
