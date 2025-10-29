from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Rating, Article, User
from ..schemas import RatingIn
from ..deps import get_current_user


router = APIRouter()


@router.post('/')
def rate(payload: RatingIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not (1 <= payload.score <= 5):
        raise HTTPException(400, detail="Score must be 1..5")
    a = db.query(Article).filter(Article.id == payload.article_id).first()
    if not a:
        raise HTTPException(404, detail="Article not found")
    existing = db.query(Rating).filter(Rating.user_id == user.id, Rating.article_id == a.id).first()
    if not existing:
        r = Rating(user_id=user.id, article_id=a.id, score=payload.score)
        db.add(r)
    else:
        existing.score = payload.score
    db.commit()
    return {"ok": True}


