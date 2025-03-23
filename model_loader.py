import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Load scaler
SCALER_PATH = "model/scaler.pkl"

def load_scaler():
    with open(SCALER_PATH, "rb") as f:
        return joblib.load(f)


# Đường dẫn tới model
MODEL_PATH = "model/CatBoost.pkl"

# Giả sử bạn có cột features như dưới (thay thế bằng đúng thứ tự cột trong training data)
feature_labels = [
    "age", "gender", "ethnicity", "education_level", "bmi", "smoking", "alcohol_consumption", "physical_activity",
    "diet_quality", "sleep_quality", "family_history_parkinsons", "traumatic_brain_injury", "hypertension",
    "diabetes", "depression", "stroke", "systolic_bp", "diastolic_bp", "cholesterol_total", "cholesterol_ldl",
    "cholesterol_hdl", "cholesterol_triglycerides", "updrs_score", "moca_score", "functional_assessment",
    "tremor", "rigidity", "bradykinesia", "postural_instability", "speech_problems", "sleep_disorders", "constipation"
]

# Load model từ file .pkl
def load_model():
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
    return model

# Định nghĩa các biến để import
best_model = load_model()
scaler = load_scaler()

