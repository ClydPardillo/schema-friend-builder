from fastapi import APIRouter
from typing import List

router = APIRouter()

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
