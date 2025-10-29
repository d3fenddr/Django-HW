from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, articles, categories, authors, reactions, ratings, bookmarks, uploads


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habr API", version="0.1.0")

# CORS: allow local dev frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(authors.router, prefix="/api/authors", tags=["authors"])
app.include_router(reactions.router, prefix="/api/reactions", tags=["reactions"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["ratings"])
app.include_router(bookmarks.router, prefix="/api/bookmarks", tags=["bookmarks"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["uploads"])


@app.get("/api/health")
def health():
    return {"status": "ok"}


