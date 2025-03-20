from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
# ✅ Schema cho tạo mới bệnh viện
class HospitalCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    established: Optional[date] = None

# ✅ Schema cho response bệnh viện
class HospitalResponse(HospitalCreate):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# ✅ Schema cho cập nhật bệnh viện
class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    established: Optional[date] = None