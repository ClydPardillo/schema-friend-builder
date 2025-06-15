
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.services import db
from app.models.user import User
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, session: Session = Depends(get_db)):
    if session.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed_pw, user_type=user.user_type)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_db)):
    db_user = session.query(User).filter_by(email=user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": db_user.id, "user_type": db_user.user_type})
    return {"access_token": token, "token_type": "bearer"}
