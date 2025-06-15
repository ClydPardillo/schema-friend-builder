
from sqlalchemy import Column, String, Text, Enum, DateTime, Integer, Boolean, ForeignKey, DECIMAL, JSON
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class OrgType(enum.Enum):
    ngo = "ngo"
    foundation = "foundation"
    religious = "religious"
    educational = "educational"
    healthcare = "healthcare"
    community = "community"
    other = "other"

class VerificationStatus(enum.Enum):
    pending = "pending"
    under_review = "under_review"
    verified = "verified"
    rejected = "rejected"
    suspended = "suspended"

class Charity(Base):
    __tablename__ = "charities"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False) 
    organization_name = Column(String(255), nullable=False)
    organization_type = Column(Enum(OrgType), nullable=False)
    registration_number = Column(String(100), unique=True)
    tax_id = Column(String(100))
    description = Column(Text)
    mission_statement = Column(Text)
    website_url = Column(String(500))
    facebook_url = Column(String(500))
    instagram_url = Column(String(500))
    twitter_url = Column(String(500))
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100), nullable=False, default='Philippines')
    verification_status = Column(Enum(VerificationStatus), nullable=False, default="pending")
    verification_date = Column(DateTime)
    verified_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    rejection_reason = Column(Text)
    bank_name = Column(String(255))
    bank_account_holder = Column(String(255))
    bank_account_number = Column(String(100))
    bank_branch_code = Column(String(50))
    bank_account_verified = Column(Boolean, nullable=False, default=False)
    bank_verification_date = Column(DateTime)
    total_raised = Column(DECIMAL(15,2), nullable=False, default=0.00)
    total_campaigns = Column(Integer, nullable=False, default=0)
    active_campaigns = Column(Integer, nullable=False, default=0)
    transparency_score = Column(Integer)
    efficiency_rating = Column(Integer)
    last_scorecard_update = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="charity")
