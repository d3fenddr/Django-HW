from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models import Article, User, Category, Reaction, Rating, Bookmark
from .. import schemas
from ..deps import get_current_user, require_staff


router = APIRouter()


def _article_out(db: Session, a: Article) -> schemas.ArticleOut:
    likes = db.query(func.count(Reaction.id)).filter(Reaction.article_id == a.id, Reaction.value == 1).scalar() or 0
    dislikes = db.query(func.count(Reaction.id)).filter(Reaction.article_id == a.id, Reaction.value == -1).scalar() or 0
    avg = db.query(func.avg(Rating.score)).filter(Rating.article_id == a.id).scalar() or 0.0
    cnt = db.query(func.count(Rating.id)).filter(Rating.article_id == a.id).scalar() or 0
    return schemas.ArticleOut(
        id=a.id,
        slug=a.slug,
        title=a.title,
        excerpt=a.excerpt,
        body=a.body,
        status=a.status,
        image_url=a.image_url,
        created_at=a.created_at,
        updated_at=a.updated_at,
        author=a.author,
        category=a.category,
        likes=likes,
        dislikes=dislikes,
        rating_avg=float(avg or 0.0),
        rating_count=int(cnt or 0),
    )


@router.get('/', response_model=List[schemas.ArticleOut])
def list_articles(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
    category_id: Optional[int] = Query(None),
):
    q = db.query(Article).join(Article.author).outerjoin(Article.category)
    if not (current_user and current_user.is_staff):
        q = q.filter(Article.status == "published")
    if category_id:
        q = q.filter(Article.category_id == category_id)
    q = q.order_by(Article.created_at.desc())
    return [_article_out(db, a) for a in q.all()]


@router.get('/popular', response_model=List[schemas.ArticleOut])
def popular_articles(db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user)):
    q = db.query(Article)
    if not (current_user and current_user.is_staff):
        q = q.filter(Article.status == "published")
    q = q.order_by(Article.created_at.desc()).all()
    result = []
    for a in q:
        avg = db.query(func.avg(Rating.score)).filter(Rating.article_id == a.id).scalar() or 0.0
        if avg and float(avg) >= 4.0:
            result.append(_article_out(db, a))
    return result


@router.get('/{slug}', response_model=schemas.ArticleOut)
def article_detail(slug: str, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user)):
    a = db.query(Article).filter(Article.slug == slug).first()
    if not a:
        raise HTTPException(404, detail="Not found")
    if not (current_user and current_user.is_staff) and a.status != "published" and (not current_user or a.author_id != current_user.id):
        raise HTTPException(403, detail="Not allowed")
    return _article_out(db, a)


def _slugify(title: str, existing: set[str]) -> str:
    base = ''.join(c if c.isalnum() or c in ['-','_'] else '-' for c in title.lower()).strip('-') or 'post'
    base = base[:200]
    slug = base
    i = 1
    while slug in existing:
        i += 1
        slug = f"{base}-{i}"
    return slug


@router.post('/', response_model=schemas.ArticleOut)
def create_article(payload: schemas.ArticleCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.category_id:
        if not db.query(Category).filter(Category.id == payload.category_id).first():
            raise HTTPException(400, detail="Invalid category")
    existing_slugs = {s for (s,) in db.query(Article.slug).all()}
    slug = _slugify(payload.title, existing_slugs)
    excerpt = (payload.body[:300] + '…') if len(payload.body) > 300 else payload.body
    status = "published" if user.is_staff else "pending"
    a = Article(
        author_id=user.id,
        title=payload.title,
        slug=slug,
        category_id=payload.category_id,
        image_url=payload.image_url,
        excerpt=excerpt,
        body=payload.body,
        status=status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return _article_out(db, a)


@router.put('/{slug}', response_model=schemas.ArticleOut)
def update_article(slug: str, payload: schemas.ArticleUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    a = db.query(Article).filter(Article.slug == slug).first()
    if not a:
        raise HTTPException(404, detail="Not found")
    if not (user.is_staff or a.author_id == user.id):
        raise HTTPException(403, detail="Not allowed")
    a.title = payload.title or a.title
    a.body = payload.body or a.body
    a.excerpt = (a.body[:300] + '…') if len(a.body) > 300 else a.body
    a.category_id = payload.category_id if payload.category_id is not None else a.category_id
    a.image_url = payload.image_url if payload.image_url is not None else a.image_url
    if user.is_staff and payload.status:
        a.status = payload.status
    else:
        a.status = "published" if user.is_staff else "pending"
    a.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(a)
    return _article_out(db, a)


@router.delete('/{slug}')
def delete_article(slug: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    a = db.query(Article).filter(Article.slug == slug).first()
    if not a:
        raise HTTPException(404, detail="Not found")
    if not (user.is_staff or a.author_id == user.id):
        raise HTTPException(403, detail="Not allowed")
    db.delete(a)
    db.commit()
    return {"ok": True}


