from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import SessionLocal
from models import Book, Author
from schemas import BookCreate, BookOut

router = APIRouter(prefix="/api/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    author = db.execute(select(Author).where(Author.id == payload.author_id)).scalars().first()
    if author is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found")
    new_book = Book(
        title=payload.title,
        pages=payload.pages,
        author_id=payload.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return BookOut.model_validate(new_book, from_attributes=True)

@router.get("/", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):
    books = db.execute(select(Book)).scalars().all()
    return [BookOut.model_validate(b, from_attributes=True) for b in books]

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.execute(select(Book).where(Book.id == book_id)).scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return BookOut.model_validate(book, from_attributes=True)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    book = db.execute(select(Book).where(Book.id == book_id)).scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    author = db.execute(select(Author).where(Author.id == payload.author_id)).scalars().first()
    if author is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author not found")
    book.title = payload.title
    book.pages = payload.pages
    book.author_id = payload.author_id
    db.commit()
    db.refresh(book)
    return BookOut.model_validate(book, from_attributes=True)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.execute(select(Book).where(Book.id == book_id)).scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
    return None
