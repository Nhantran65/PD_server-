from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Hospital
from schemas import HospitalCreate, HospitalResponse, HospitalUpdate
from typing import List
from auth_utils import verify_token  # Import middleware xác thực


print("✅ hospitals.py has been loaded successfully!")

router = APIRouter()

# 📌 1. API tạo mới một bệnh viện
@router.post("/", response_model=HospitalResponse)
def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    existing_hospital = db.query(Hospital).filter(Hospital.name == hospital.name).first()
    if existing_hospital:
        raise HTTPException(status_code=400, detail="Hospital already exists")
    
    new_hospital = Hospital(
        name=hospital.name,
        description=hospital.description,
        address=hospital.address,
        phone=hospital.phone,
        email=hospital.email,
        website=hospital.website,
        established=hospital.established
    )
    
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    
    return new_hospital

# 🔐 Yêu cầu Authentication để lấy danh sách bệnh viện
@router.get("/", response_model=List[HospitalResponse])
def get_hospitals(db: Session = Depends(get_db), token: dict = Depends(verify_token)):
    hospitals = db.query(Hospital).all()
    return hospitals

# 📌 3. API lấy thông tin bệnh viện theo ID
@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital

# 📌 4. API cập nhật thông tin bệnh viện
@router.put("/{hospital_id}", response_model=HospitalResponse)
def update_hospital(hospital_id: int, hospital_update: HospitalUpdate, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    for key, value in hospital_update.dict(exclude_unset=True).items():
        setattr(hospital, key, value)
    
    db.commit()
    db.refresh(hospital)
    
    return hospital

# 📌 5. API xóa bệnh viện
@router.delete("/{hospital_id}")
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    db.delete(hospital)
    db.commit()
    
    return {"message": "Hospital deleted successfully"}
