
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserType(str, Enum):
    donor = "donor"
    charity = "charity"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_type: UserType

class UserOut(BaseModel):
    id: str
    email: EmailStr
    user_type: UserType
    is_active: bool

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
