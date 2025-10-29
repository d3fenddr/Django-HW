from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Bookmark, Article, User
from ..schemas import BookmarkIn, ArticleOut
from ..deps import get_current_user
from .articles import _article_out
from typing import List


router = APIRouter()


@router.post('/toggle')
def toggle_bookmark(payload: BookmarkIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    a = db.query(Article).filter(Article.id == payload.article_id).first()
    if not a:
        raise HTTPException(404, detail="Article not found")
    existing = db.query(Bookmark).filter(Bookmark.user_id == user.id, Bookmark.article_id == a.id).first()
    if existing:
        db.delete(existing)
    else:
        db.add(Bookmark(user_id=user.id, article_id=a.id))
    db.commit()
    return {"ok": True}


@router.get('/', response_model=List[ArticleOut])
def my_bookmarks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Article).join(Bookmark, Bookmark.article_id == Article.id).filter(Bookmark.user_id == user.id)
    return [_article_out(db, a) for a in q.all()]


