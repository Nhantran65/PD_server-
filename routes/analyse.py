# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from models import MedicalExaminationForm
# import lime.lime_tabular
# import numpy as np
# from fastapi.responses import FileResponse
# import os
# import pickle

# router = APIRouter()

# # Load model CatBoost từ file
# with open("model/CatBoost.pkl", "rb") as model_file:
#     model = pickle.load(model_file)

# @router.get("/analyse/{exam_id}")
# def analyse_examination(exam_id: int, db: Session = Depends(get_db)):
#     """
#     Phân tích kết quả dự đoán bằng LIME.
#     """
#     exam = db.query(MedicalExaminationForm).filter(MedicalExaminationForm.id == exam_id).first()
#     if not exam:
#         raise HTTPException(status_code=404, detail="Medical Examination not found")

#     features = np.array([
#         exam.age, exam.gender, exam.ethnicity, exam.education_level,
#         exam.bmi, exam.smoking, exam.alcohol_consumption, exam.physical_activity,
#         exam.diet_quality, exam.sleep_quality,
#         exam.family_history_parkinsons, exam.traumatic_brain_injury, exam.hypertension,
#         exam.diabetes, exam.depression, exam.stroke,
#         exam.systolic_bp, exam.diastolic_bp, exam.cholesterol_total, 
#         exam.cholesterol_ldl, exam.cholesterol_hdl, exam.cholesterol_triglycerides,
#         exam.updrs_score, exam.moca_score, exam.functional_assessment,
#         exam.tremor, exam.rigidity, exam.bradykinesia, exam.postural_instability,
#         exam.speech_problems, exam.sleep_disorders, exam.constipation
#     ]).reshape(1, -1)

#     # Tạo LIME explainer
#     lime_explainer = lime.lime_tabular.LimeTabularExplainer(
#         training_data=features, 
#         feature_names=list(exam.__dict__.keys())[4:], 
#         class_names=["No PD", "PD"],
#         discretize_continuous=True
#     )

#     explanation = lime_explainer.explain_instance(features[0], model.predict_proba, num_features=10)

#     # Lưu kết quả phân tích ra file HTML
#     explanation.save_to_file("lime_analysis.html")
#     return FileResponse("lime_analysis.html")
