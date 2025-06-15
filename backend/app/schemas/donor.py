
from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime, date

class PaymentMethod(str, Enum):
    gcash = "gcash"
    paymaya = "paymaya"
    card = "card"
    bank = "bank"

class DonationFrequencyPreference(str, Enum):
    onetime = "onetime"
    monthly = "monthly"
    both = "both"

class DonorCreate(BaseModel):
    user_id: str
    date_of_birth: Optional[date]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str] = "Philippines"
    preferred_payment_method: Optional[PaymentMethod]
    donation_frequency_preference: Optional[DonationFrequencyPreference] = "onetime"
    favorite_categories: Optional[List[str]]
    notification_preferences: Optional[Dict]
    tax_receipt_required: Optional[bool] = True

class DonorOut(DonorCreate):
    id: str
    total_donated: float
    donation_count: int
    created_at: datetime
    updated_at: datetime
