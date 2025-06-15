
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class OrgType(str, Enum):
    ngo = "ngo"
    foundation = "foundation"
    religious = "religious"
    educational = "educational"
    healthcare = "healthcare"
    community = "community"
    other = "other"

class VerificationStatus(str, Enum):
    pending = "pending"
    under_review = "under_review"
    verified = "verified"
    rejected = "rejected"
    suspended = "suspended"

class CharityCreate(BaseModel):
    user_id: str
    organization_name: str
    organization_type: OrgType
    registration_number: Optional[str]
    tax_id: Optional[str]
    description: Optional[str]
    mission_statement: Optional[str]
    website_url: Optional[str]
    facebook_url: Optional[str]
    instagram_url: Optional[str]
    twitter_url: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str] = "Philippines"
    bank_name: Optional[str]
    bank_account_holder: Optional[str]
    bank_account_number: Optional[str]
    bank_branch_code: Optional[str]
    # other optional fields as needed

class CharityOut(CharityCreate):
    id: str
    verification_status: VerificationStatus
    created_at: datetime
    updated_at: datetime
