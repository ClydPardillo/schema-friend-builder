
from sqlalchemy import Column, String, Text, Enum, DateTime, Integer, Boolean, ForeignKey, DECIMAL, JSON
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class CampaignStatus(enum.Enum):
    draft = "draft"
    pending_approval = "pending_approval"
    active = "active"
    paused = "paused"
    completed = "completed"
    cancelled = "cancelled"
    expired = "expired"

class CampaignVerificationStatus(enum.Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True)
    charity_id = Column(String(36), ForeignKey("charities.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500))
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    goal_amount = Column(DECIMAL(15,2), nullable=False)
    raised_amount = Column(DECIMAL(15,2), nullable=False, default=0.00)
    held_amount = Column(DECIMAL(15,2), nullable=False, default=0.00)
    released_amount = Column(DECIMAL(15,2), nullable=False, default=0.00)
    image_url = Column(String(500))
    banner_url = Column(String(500))
    video_url = Column(String(500))
    location = Column(String(255))
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(CampaignStatus), nullable=False, default="draft")
    verification_status = Column(Enum(CampaignVerificationStatus), nullable=False, default="pending")
    verified = Column(Boolean, nullable=False, default=False)
    verified_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    verified_at = Column(DateTime)
    rejection_reason = Column(Text)
    featured = Column(Boolean, nullable=False, default=False)
    urgent = Column(Boolean, nullable=False, default=False)
    donor_count = Column(Integer, nullable=False, default=0)
    view_count = Column(Integer, nullable=False, default=0)
    share_count = Column(Integer, nullable=False, default=0)
    tags = Column(JSON)
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
