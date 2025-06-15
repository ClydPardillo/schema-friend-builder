
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from app.models.base import Base
import enum

class UserType(enum.Enum):
    donor = 'donor'
    charity = 'charity'
    admin = 'admin'

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    is_active = Column(Boolean, default=True)
