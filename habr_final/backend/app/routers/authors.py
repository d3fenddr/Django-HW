from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Article
from ..schemas import UserOut, ArticleOut
from sqlalchemy import func
from typing import List


router = APIRouter()


@router.get('/', response_model=List[UserOut])
def list_authors(db: Session = Depends(get_db)):
    users = db.query(User).join(Article, isouter=True).group_by(User.id).having(func.count(Article.id) > 0).all()
    return users


@router.get('/{user_id}', response_model=List[ArticleOut])
def author_articles(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="Author not found")
    from .articles import _article_out
    arts = db.query(Article).filter(Article.author_id == user_id, Article.status == "published").order_by(Article.created_at.desc()).all()
    return [_article_out(db, a) for a in arts]


