
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/google")
def google_login():
    return {"message": "OAuth2 not implemented. Add real redirect logic here."}

@router.get("/auth/facebook")
def facebook_login():
    return {"message": "OAuth2 not implemented. Add real redirect logic here."}
