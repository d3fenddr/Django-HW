from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Reaction, Article, User
from ..schemas import ReactionIn
from ..deps import get_current_user


router = APIRouter()


@router.post('/')
def react(payload: ReactionIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.value not in (1, -1):
        raise HTTPException(400, detail="Invalid value")
    a = db.query(Article).filter(Article.id == payload.article_id).first()
    if not a:
        raise HTTPException(404, detail="Article not found")
    existing = db.query(Reaction).filter(Reaction.user_id == user.id, Reaction.article_id == a.id).first()
    if not existing:
        r = Reaction(user_id=user.id, article_id=a.id, value=payload.value)
        db.add(r)
    else:
        if existing.value == payload.value:
            db.delete(existing)
        else:
            existing.value = payload.value
    db.commit()
    return {"ok": True}


