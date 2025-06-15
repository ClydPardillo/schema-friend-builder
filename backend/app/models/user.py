
from sqlalchemy import Column, String, Boolean, Enum, DateTime, Text, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class UserType(enum.Enum):
    donor = "donor"
    charity = "charity"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    profile_image_url = Column(String(500))
    email_verified = Column(Boolean, nullable=False, default=False)
    email_verified_at = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login_at = Column(DateTime)
    password_reset_token = Column(String(255))
    password_reset_expires = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # relationships
    donor = relationship("Donor", uselist=False, back_populates="user")
    charity = relationship("Charity", uselist=False, back_populates="user")

