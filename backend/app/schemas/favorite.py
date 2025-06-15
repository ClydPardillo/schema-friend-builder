
from pydantic import BaseModel
from typing import List

class FavoriteCreate(BaseModel):
    campaign_id: str

class FavoriteOut(BaseModel):
    id: str
    user_id: str
    campaign_id: str

    class Config:
        orm_mode = True

class FavoriteListOut(BaseModel):
    favorites: List[FavoriteOut]
