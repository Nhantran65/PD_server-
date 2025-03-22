from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import MedicalExaminationForm
from schemas import MedicalExaminationResponse

router = APIRouter()

@router.get("/", response_model=list[MedicalExaminationResponse])
def get_all_examinations(db: Session = Depends(get_db)):
    """
    Lấy tất cả Medical Examination Forms.
    """
    exams = db.query(MedicalExaminationForm).all()
    return exams  # Lấy tất cả, đã bao gồm diagnosis

@router.get("/{exam_id}", response_model=MedicalExaminationResponse)
def get_examination_by_id(exam_id: int, db: Session = Depends(get_db)):
    """
    Lấy Medical Examination Form theo ID.
    """
    exam = db.query(MedicalExaminationForm).filter(MedicalExaminationForm.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Examination not found")
    return exam  # Lấy theo ID, đã bao gồm diagnosis
