from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import DoctorDecision, Result
from schemas import DoctorDecisionCreate, DoctorDecisionResponse
from typing import List

router = APIRouter(prefix="/doctor-decisions", tags=["Doctor Decisions"])


# ✅ Tạo mới quyết định bác sĩ
@router.post("/", response_model=DoctorDecisionResponse, summary="Tạo quyết định của bác sĩ")
def create_doctor_decision(decision: DoctorDecisionCreate, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == decision.result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Không tìm thấy kết quả (result) tương ứng")

    doctor_decision = DoctorDecision(**decision.dict())
    db.add(doctor_decision)
    db.commit()
    db.refresh(doctor_decision)
    return doctor_decision


# ✅ Lấy tất cả quyết định bác sĩ
@router.get("/", response_model=List[DoctorDecisionResponse], summary="Lấy tất cả quyết định bác sĩ")
def get_all_doctor_decisions(db: Session = Depends(get_db)):
    return db.query(DoctorDecision).all()


# ✅ Lấy 1 quyết định bác sĩ theo ID
@router.get("/{id}", response_model=DoctorDecisionResponse, summary="Lấy quyết định bác sĩ theo ID")
def get_doctor_decision(id: int, db: Session = Depends(get_db)):
    decision = db.query(DoctorDecision).filter(DoctorDecision.id == id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Không tìm thấy quyết định")
    return decision


# ✅ Cập nhật quyết định bác sĩ
@router.put("/{id}", response_model=DoctorDecisionResponse, summary="Cập nhật quyết định bác sĩ")
def update_doctor_decision(id: int, update_data: DoctorDecisionCreate, db: Session = Depends(get_db)):
    decision = db.query(DoctorDecision).filter(DoctorDecision.id == id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Không tìm thấy quyết định")
    
    decision.result_id = update_data.result_id
    decision.doctor_decision = update_data.doctor_decision
    db.commit()
    db.refresh(decision)
    return decision


# ✅ Xoá quyết định bác sĩ
@router.delete("/{id}", summary="Xoá quyết định bác sĩ theo ID")
def delete_doctor_decision(id: int, db: Session = Depends(get_db)):
    decision = db.query(DoctorDecision).filter(DoctorDecision.id == id).first()
    if not decision:
        raise HTTPException(status_code=404, detail="Không tìm thấy quyết định")
    
    db.delete(decision)
    db.commit()
    return {"message": "Đã xoá thành công"}
