from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import MedicalExaminationForm, Status
from schemas import MedicalExaminationCreate, MedicalExaminationResponse
import pickle
import numpy as np

router = APIRouter()

# Load model CatBoost từ file
with open("model/CatBoost.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@router.post("/", response_model=MedicalExaminationResponse)
def create_examination(exam_data: MedicalExaminationCreate, db: Session = Depends(get_db)):
    """
    Tạo mới Medical Examination Form, dự đoán kết quả Parkinson trước khi lưu vào Database.
    """
    # Trích xuất 32 features cho model
    features = np.array([
        exam_data.age, exam_data.gender, exam_data.ethnicity, exam_data.education_level,
        exam_data.bmi, exam_data.smoking, exam_data.alcohol_consumption, exam_data.physical_activity,
        exam_data.diet_quality, exam_data.sleep_quality,
        exam_data.family_history_parkinsons, exam_data.traumatic_brain_injury, exam_data.hypertension,
        exam_data.diabetes, exam_data.depression, exam_data.stroke,
        exam_data.systolic_bp, exam_data.diastolic_bp, exam_data.cholesterol_total, 
        exam_data.cholesterol_ldl, exam_data.cholesterol_hdl, exam_data.cholesterol_triglycerides,
        exam_data.updrs_score, exam_data.moca_score, exam_data.functional_assessment,
        exam_data.tremor, exam_data.rigidity, exam_data.bradykinesia, exam_data.postural_instability,
        exam_data.speech_problems, exam_data.sleep_disorders, exam_data.constipation
    ]).reshape(1, -1)

    # Dự đoán kết quả
    prediction = model.predict(features)[0]  # 0: Không bị Parkinson, 1: Có Parkinson

    print(bool(prediction))
    # Lưu thông tin vào database
    new_exam = MedicalExaminationForm(
        **exam_data.dict(),
        diagnosis=bool(prediction)  # Thêm giá trị diagnosis vào database
    )
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    # Cập nhật Status thành "PREDICTED"
    predicted_status = db.query(Status).filter(Status.name == "PREDICTED").first()
    if predicted_status:
        new_exam.status_id = predicted_status.id
        db.commit()

    # Trả về toàn bộ thông tin, có thêm `diagnosis`
    return {
        **exam_data.dict(),
        "id": new_exam.id,
        "status_id": new_exam.status_id,
        "diagnosis": bool(prediction)  # Trả về kết quả chẩn đoán
    }