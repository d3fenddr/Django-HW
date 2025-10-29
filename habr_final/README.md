Habr Clone - Django + FastAPI API + React Frontend

Structure (this directory only)
- backend/ — FastAPI + SQLAlchemy API (JWT auth, Cloudinary uploads)
- frontend/ — React (Vite) app consuming the API

Backend (FastAPI)
1) Create and activate a virtualenv (optional) and install deps:
   cd backend
   pip install -r requirements.txt

2) Configure environment (copy and adjust):
   set HABR_API_DATABASE_URL=sqlite:///./habr_api.db
   set HABR_API_JWT_SECRET=change-me
   set HABR_API_JWT_EXPIRES_MIN=120
   set CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>

3) Run the API:
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

API highlights
- POST /api/auth/register — create user (username, email, password)
- POST /api/auth/login (form) — returns bearer token
- GET /api/articles — list (published for guests/users; all for staff)
- GET /api/articles/popular — rating >= 4.0
- GET /api/articles/{slug} — detail
- POST /api/articles — create (auth; staff auto-publish, others pending)
- PUT /api/articles/{slug} — edit (author or staff; author sets pending)
- DELETE /api/articles/{slug} — delete (author or staff)
- POST /api/reactions — like/dislike toggle
- POST /api/ratings — rate 1..5 (updates if exists)
- GET /api/categories — predefined categories
- GET /api/authors — list authors with articles
- GET /api/authors/{id} — articles by author (published)
- POST /api/bookmarks/toggle — toggle bookmark
- GET /api/bookmarks — my bookmarks
- POST /api/uploads/image — upload image to Cloudinary (auth)

Frontend (React)
1) Install and run:
   cd frontend
   npm install
   npm run dev

Dev URLs
- Frontend: http://localhost:5173
- API: http://127.0.0.1:8000 (proxied via Vite for /api)

Auth
- On login, token is stored in localStorage under key habr_token and automatically added to Authorization header.

Notes
- Initial categories can be inserted directly into DB or served by Django if you prefer. You can also add a tiny bootstrap script for categories if needed.

