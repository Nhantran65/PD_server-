from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import DoctorDecision, Result
from schemas import DoctorDecisionCreate, DoctorDecisionResponse
from typing import List

router = APIRouter(prefix="/doctor-decisions", tags=["Doctor Decisions"])


# ✅ Tạo mới quyết định bác sĩ
@router.post("/", response_model=DoctorDecisionResponse, summary="Create a physician decision")
def create_doctor_decision(decision: DoctorDecisionCreate, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == decision.result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="No matching results found")

    doctor_decision = DoctorDecision(**decision.dict())
    db.add(doctor_decision)
    db.commit()
    db.refresh(doctor_decision)
    return doctor_decision


# ✅ Lấy tất cả quyết định bác sĩ
@router.get("/", response_model=List[DoctorDecisionResponse], summary="Get all the doctor's decisions")
def get_all_doctor_decisions(db: Session = Depends(get_db)):
    return db.query(DoctorDecision).all()


# ✅ Lấy 1 quyết định bác sĩ theo ID
@router.get("/{id}", response_model=DoctorDecisionResponse, summary="Get doctor's decision by ID")
def get_doctor_decision(id: int, db: Session = Depends(get_db)):
    decision = db.query(DoctorDecision).filter(DoctorDecision.id == id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="No decision found")
    return decision


# ✅ Cập nhật quyết định bác sĩ
@router.put("/{id}", response_model=DoctorDecisionResponse, summary="Update doctor's decision")
def update_doctor_decision(id: int, update_data: DoctorDecisionCreate, db: Session = Depends(get_db)):
    decision = db.query(DoctorDecision).filter(DoctorDecision.id == id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="No decision found")
    
    decision.result_id = update_data.result_id
    decision.doctor_decision = update_data.doctor_decision
    db.commit()
    db.refresh(decision)
    return decision


# ✅ Xoá quyết định bác sĩ
@router.delete("/{id}", summary="Delete doctor decision by ID")
def delete_doctor_decision(id: int, db: Session = Depends(get_db)):
    decision = db.query(DoctorDecision).filter(DoctorDecision.id == id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="No doctor's decision found")
    
    db.delete(decision)
    db.commit()
    return {"message": "Deleted Successfully"}
