from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("HABR_API_JWT_SECRET", "dev-secret")
JWT_ALG = "HS256"
JWT_EXPIRES_MIN = int(os.getenv("HABR_API_JWT_EXPIRES_MIN", "60"))

def _prehash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
    prehashed = _prehash(password)
    return pwd_context.hash(prehashed)

def verify_password(password: str, password_hash: str) -> bool:
    prehashed = _prehash(password)
    return pwd_context.verify(prehashed, password_hash)

def create_access_token(sub: str) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRES_MIN)).timestamp()),
        "type": "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        return None
