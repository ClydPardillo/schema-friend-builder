
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime

class CampaignStatus(str, Enum):
    draft = "draft"
    pending_approval = "pending_approval"
    active = "active"
    paused = "paused"
    completed = "completed"
    cancelled = "cancelled"
    expired = "expired"

class CampaignVerificationStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class CampaignCreate(BaseModel):
    charity_id: str
    title: str
    slug: str
    description: str
    short_description: Optional[str]
    category: str
    subcategory: Optional[str]
    goal_amount: float
    end_date: datetime
    start_date: Optional[datetime]
    image_url: Optional[str]
    banner_url: Optional[str]
    video_url: Optional[str]
    location: Optional[str]
    status: Optional[CampaignStatus] = "draft"
    verification_status: Optional[CampaignVerificationStatus] = "pending"
    featured: Optional[bool] = False
    urgent: Optional[bool] = False
    tags: Optional[List[str]]
    meta_title: Optional[str]
    meta_description: Optional[str]

class CampaignOut(CampaignCreate):
    id: str
    raised_amount: float
    held_amount: float
    released_amount: float
    verified: bool
    donor_count: int
    view_count: int
    share_count: int
    created_at: datetime
    updated_at: datetime
