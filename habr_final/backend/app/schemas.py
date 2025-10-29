from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    is_staff: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    title: str
    body: str
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    status: Optional[str] = None


class ArticleOut(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    body: str
    status: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: UserOut
    category: Optional[CategoryOut] = None
    likes: int
    dislikes: int
    rating_avg: float
    rating_count: int

    class Config:
        from_attributes = True


class ReactionIn(BaseModel):
    article_id: int
    value: int  # 1 or -1


class RatingIn(BaseModel):
    article_id: int
    score: int


class BookmarkIn(BaseModel):
    article_id: int


