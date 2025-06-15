
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services import db
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteOut, FavoriteListOut
from app.routes.user import get_current_user
import uuid

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/favorites", response_model=FavoriteOut)
def add_favorite(payload: FavoriteCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = session.query(Favorite).filter_by(user_id=current_user.id, campaign_id=payload.campaign_id).first()
    if fav:
        raise HTTPException(status_code=400, detail="Campaign already favorited")
    favorite = Favorite(id=str(uuid.uuid4()), user_id=current_user.id, campaign_id=payload.campaign_id)
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite

@router.delete("/favorites/{campaign_id}", response_model=dict)
def remove_favorite(campaign_id: str, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = session.query(Favorite).filter_by(user_id=current_user.id, campaign_id=campaign_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    session.delete(fav)
    session.commit()
    return {"success": True, "message": "Favorite removed"}

@router.get("/favorites", response_model=FavoriteListOut)
def get_favorites(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favorites = session.query(Favorite).filter_by(user_id=current_user.id).all()
    return {"favorites": favorites}
