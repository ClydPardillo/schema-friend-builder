
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.donor import DonorCreate, DonorOut
from app.services import db
from app.models.donor import Donor
from typing import List

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=DonorOut)
def create_donor(donor: DonorCreate, session: Session = Depends(get_db)):
    db_donor = Donor(**donor.dict())
    session.add(db_donor)
    session.commit()
    session.refresh(db_donor)
    return db_donor

@router.get("/", response_model=List[DonorOut])
def list_donors(skip: int = 0, limit: int = 20, session: Session = Depends(get_db)):
    donors = session.query(Donor).offset(skip).limit(limit).all()
    return donors

@router.get("/{donor_id}", response_model=DonorOut)
def get_donor(donor_id: str, session: Session = Depends(get_db)):
    donor = session.query(Donor).filter_by(id=donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor
