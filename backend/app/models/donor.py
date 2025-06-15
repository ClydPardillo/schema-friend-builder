
from sqlalchemy import Column, String, Enum, Date, DateTime, Integer, DECIMAL, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from app.models.base import Base
import enum

class PaymentMethod(enum.Enum):
    gcash = "gcash"
    paymaya = "paymaya"
    card = "card"
    bank = "bank"

class DonationFrequencyPreference(enum.Enum):
    onetime = "onetime"
    monthly = "monthly"
    both = "both"

class Donor(Base):
    __tablename__ = "donors"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    date_of_birth = Column(Date)
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100), nullable=False, default='Philippines')
    preferred_payment_method = Column(Enum(PaymentMethod))
    donation_frequency_preference = Column(Enum(DonationFrequencyPreference), nullable=False, default="onetime")
    total_donated = Column(DECIMAL(15,2), nullable=False, default=0.00)
    donation_count = Column(Integer, nullable=False, default=0)
    favorite_categories = Column(JSON)
    notification_preferences = Column(JSON)
    tax_receipt_required = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="donor")
