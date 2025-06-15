from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.services import db
from app.models.user import User
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from typing import Any, Optional
import uuid
from datetime import datetime, timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please provide a valid token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> User:
    user = get_current_user(token, session)
    if user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Admin privilege required")
    return user

@router.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_db)) -> Any:
    existing = session.query(User).filter_by(email=user.email).first()
    if existing:
        return {
            "success": False,
            "message": "Email already registered",
            "data": None
        }
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed_pw, user_type=user.user_type)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    out = {
        "success": True,
        "message": "Account created successfully.",
        "data": {
            "id": db_user.id,
            "email": db_user.email,
            "user_type": db_user.user_type.value,
            "is_active": db_user.is_active
        }
    }
    return out

@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_db)) -> Any:
    db_user = session.query(User).filter_by(email=user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        return {
            "success": False,
            "message": "Invalid credentials",
            "data": None
        }
    token = create_access_token({"user_id": db_user.id, "user_type": db_user.user_type.value})
    return {
        "success": True,
        "message": "Login successful.",
        "data": {
            "access_token": token,
            "token_type": "bearer"
        }
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "message": "User profile retrieved.",
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "user_type": current_user.user_type.value,
            "is_active": current_user.is_active
        }
    }

@router.post("/forgot-password")
def forgot_password(email: str = Body(..., embed=True), session: Session = Depends(get_db)):
    user = session.query(User).filter_by(email=email).first()
    if not user:
        # Avoid info leaks; always return success
        return {"success": True, "message": "If your email exists, you will get a reset link."}
    token = str(uuid.uuid4())
    user.password_reset_token = token
    user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
    session.commit()
    # Send reset link via email. See docs for provider integration.
    try:
        # Mock email: show how to replace with e.g. SendGrid, SMTP, etc
        # Uncomment/send in production
        # send_reset_email(user.email, token)
        print(f"[SEND EMAIL] Would send to {user.email} — Reset link: https://yourapp.com/reset-password?token={token}")
        email_sent = True  # TODO: Integrate with real provider
    except Exception as e:
        return {"success": False, "message": "Failed to send reset email. Please try again later."}
    return {
        "success": True,
        "message": "If your email exists, you will get a reset link."
    }
    
# Example placeholder for email sending
def send_reset_email(to_email: str, token: str):
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["Subject"] = "Your password reset link"
    msg["From"] = "noreply@clearcause.com"
    msg["To"] = to_email
    msg.set_content(
        f"Hi,\n\nClick below to reset your password:\nhttps://yourapp.com/reset-password?token={token}\n\nIf you did not request..."
    )
    # SMTP setup (adjust for your provider)
    with smtplib.SMTP("smtp.yourprovider.com", 587) as server:
        server.starttls()
        server.login("username", "password")
        server.send_message(msg)
    print(f"Email sent to {to_email}")

@router.post("/reset-password")
def reset_password(token: str = Body(...), new_password: str = Body(...), session: Session = Depends(get_db)):
    user = session.query(User).filter_by(password_reset_token=token).first()
    if not user or not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
        return {"success": False, "message": "Invalid or expired token."}
    from app.auth.password import hash_password
    user.password_hash = hash_password(new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    session.commit()
    return {"success": True, "message": "Password reset successful."}
