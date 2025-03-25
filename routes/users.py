from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserResponse

router = APIRouter()

@router.get("/doctors", response_model=list[UserResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    doctors = db.query(User).filter(User.role == "doctor").all()
    return [UserResponse.from_orm(doc) for doc in doctors]  # ✅

@router.get("/patients", response_model=list[UserResponse])
def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(User).filter(User.role == "patient").all()
    return [UserResponse.from_orm(p) for p in patients]  # ✅
