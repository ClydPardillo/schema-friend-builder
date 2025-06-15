from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class UserType(str, Enum):
    donor = "donor"
    charity = "charity"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_type: UserType
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    user_type: UserType
    is_active: bool
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    profile_image_url: Optional[str]
    email_verified: bool
    email_verified_at: Optional[datetime]
    last_login_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
