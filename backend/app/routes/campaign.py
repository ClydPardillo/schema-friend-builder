from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.services import db
from app.models.campaign import Campaign, CampaignStatus, CampaignVerificationStatus
from app.schemas.campaign import CampaignOut
from app.routes.user import get_current_admin, get_current_user

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.get("/")
def list_campaigns():
    data = [
        {"id": "1", "title": "Clean Water Project", "status": "active", "target": 10000},
        {"id": "2", "title": "Books for Kids", "status": "completed", "target": 2500}
    ]
    return {
        "success": True,
        "message": "Campaigns fetched successfully.",
        "data": data
    }

@router.post("/admin/campaigns/{id}/approve")
def approve_campaign(id: str, session: Session = Depends(get_db), admin=Depends(get_current_admin)):
    campaign = session.query(Campaign).filter_by(id=id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Not found")
    campaign.status = CampaignStatus.active
    campaign.verification_status = CampaignVerificationStatus.verified
    campaign.verified = True
    session.commit()
    return {
        "success": True,
        "message": "Campaign approved",
        "data": CampaignOut.from_orm(campaign)
    }

@router.post("/admin/campaigns/{id}/reject")
def reject_campaign(id: str, session: Session = Depends(get_db), admin=Depends(get_current_admin)):
    campaign = session.query(Campaign).filter_by(id=id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Not found")
    campaign.status = CampaignStatus.rejected
    campaign.verification_status = CampaignVerificationStatus.rejected
    campaign.verified = False
    campaign.rejection_reason = "Rejected by admin"  # real app: get from request
    session.commit()
    return {
        "success": True,
        "message": "Campaign rejected",
        "data": CampaignOut.from_orm(campaign)
    }
