from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Dict, Any

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    first_name:  Optional[str] = None
    last_name:  Optional[str] = None
    email: str
    role: str

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

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

# ✅ Schema tạo mới Status
class StatusCreate(BaseModel):
    name: str

# ✅ Schema response cho Status
class StatusResponse(StatusCreate):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

# ✅ Schema cập nhật Status
class StatusUpdate(BaseModel):
    name: Optional[str] = None

class MedicalExaminationCreate(BaseModel):
    doctor_id: int
    patient_id: int
    hospital_id: int
    status_id: int = 1  # Mặc định khi tạo mới là "PENDING"

    age: int
    gender: bool
    ethnicity: int
    education_level: int

    bmi: float
    smoking: bool
    alcohol_consumption: float
    physical_activity: float
    diet_quality: float
    sleep_quality: float

    family_history_parkinsons: bool
    traumatic_brain_injury: bool
    hypertension: bool
    diabetes: bool
    depression: bool
    stroke: bool

    systolic_bp: int
    diastolic_bp: int
    cholesterol_total: float
    cholesterol_ldl: float
    cholesterol_hdl: float
    cholesterol_triglycerides: float

    updrs_score: float
    moca_score: float
    functional_assessment: float

    tremor: bool
    rigidity: bool
    bradykinesia: bool
    postural_instability: bool
    speech_problems: bool
    sleep_disorders: bool
    constipation: bool


class MedicalExaminationResponse(MedicalExaminationCreate):
    id: int
    diagnosis: bool

    class Config:
        orm_mode = True

class ResultCreate(BaseModel):
    medical_examination_form_id: int
    lime_result_html: Optional[Dict[str, Any]] = None

class ResultResponse(ResultCreate):
    id: int

    class Config:
        orm_mode = True