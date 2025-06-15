
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_campaigns():
    # Implement DB fetch here
    return [{"id": "1", "title": "Sample Campaign"}]
