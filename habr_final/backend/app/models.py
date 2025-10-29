from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, SmallInteger, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(254), unique=True, index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    articles = relationship("Article", back_populates="author")


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    articles = relationship("Article", back_populates="category")


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    excerpt: Mapped[str] = mapped_column(Text, default="")
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(12), default="pending")  # pending|published
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="articles")
    category = relationship("Category", back_populates="articles")
    reactions = relationship("Reaction", back_populates="article", cascade="all, delete")
    ratings = relationship("Rating", back_populates="article", cascade="all, delete")
    bookmarks = relationship("Bookmark", back_populates="article", cascade="all, delete")


class Reaction(Base):
    __tablename__ = "reactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    value: Mapped[int] = mapped_column(SmallInteger)  # 1 like, -1 dislike
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    article = relationship("Article", back_populates="reactions")
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uix_reaction_user_article"),
    )


class Rating(Base):
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    score: Mapped[int] = mapped_column(SmallInteger)  # 1..5
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    article = relationship("Article", back_populates="ratings")
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uix_rating_user_article"),
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    article = relationship("Article", back_populates="bookmarks")
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uix_bookmark_user_article"),
    )


