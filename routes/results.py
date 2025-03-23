from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import MedicalExaminationForm, Result
import json
import numpy as np
import lime.lime_tabular
from model_loader import best_model, scaler, feature_labels  # Ensure you have best_model & scaler loaded

router = APIRouter()

@router.post("/results/lime/{examination_id}")
def generate_lime_result(examination_id: int, db: Session = Depends(get_db)):
    # 1. Lấy thông tin từ DB
    form = db.query(MedicalExaminationForm).filter_by(id=examination_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Medical examination form not found")

    # 2. Tạo vector input từ form (đảm bảo đúng thứ tự feature_labels)
    form_dict = form.__dict__
    input_data = np.array([[form_dict[feature] for feature in feature_labels]])
    scaled_input = scaler.transform(input_data)

    # 3. Tạo LIME explanation
    explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=scaler.transform([np.zeros(len(feature_labels))]),
        feature_names=feature_labels,
        class_names=["No PD", "PD"],
        discretize_continuous=True
    )

    explanation = explainer.explain_instance(
        scaled_input[0],
        best_model.predict_proba,
        num_features=10
    )

    # 4. Trích xuất thông tin
    pred_probs = explanation.predict_proba
    class_names = explanation.class_names
    predicted_class = class_names[np.argmax(pred_probs)]
    prob_dict = {class_names[i]: float(prob) for i, prob in enumerate(pred_probs)}

    explanation_full = []
    for feat, weight in explanation.as_list():
        side = "PD" if weight > 0 else "No PD"
        explanation_full.append({
            "feature": feat,
            "weight": float(weight),
            "side": side
        })

    raw_feature_values = {feature_labels[i]: float(scaled_input[0][i]) for i in range(len(feature_labels))}

    lime_json = {
        "prediction_probabilities": prob_dict,
        "predicted_class": predicted_class,
        "explanation": explanation_full,
        "raw_feature_values": raw_feature_values,
        "sample_index": examination_id
    }

    # 5. Lưu vào DB
    result = Result(
        medical_examination_form_id=examination_id,
        lime_result_html=json.dumps(lime_json, indent=4)
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return {"message": "✅ LIME result saved successfully", "result_id": result.id, "lime_result": lime_json}


@router.get("/", summary="Lấy tất cả kết quả LIME")
def get_all_results(db: Session = Depends(get_db)):
    results = db.query(Result).all()
    return [
        {
            "result_id": r.id,
            "medical_examination_form_id": r.medical_examination_form_id,
            "lime_result": json.loads(r.lime_result_html) if r.lime_result_html else None
        }
        for r in results
    ]

@router.get("/{id}", summary="Lấy kết quả LIME theo ID")
def get_result_by_id(id: int, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return {
        "result_id": result.id,
        "medical_examination_form_id": result.medical_examination_form_id,
        "lime_result": json.loads(result.lime_result_html) if result.lime_result_html else None
    }